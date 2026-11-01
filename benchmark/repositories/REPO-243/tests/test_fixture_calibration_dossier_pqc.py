"""Application and crypto tests for FixtureCalibrationDossier PQC reference."""
import json, pytest
from fixture_calibration_dossier_pqc.domain import validate_record, canonical_record, transition_record
from fixture_calibration_dossier_pqc.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, generate_recipient, seal_artifact, open_artifact

RECORD={"record_id": "cal-243", "fixture_id": "fixture-jig-9", "measured_error_microns": 37, "calibration_revision": 12, "technician_id": "tech-31", "state": "scheduled"}
def test_domain_record_and_lifecycle():
    assert validate_record(RECORD)==RECORD
    assert canonical_record(RECORD)==canonical_record(dict(RECORD))
    changed=transition_record(RECORD,'measured')
    assert changed["state"]!='scheduled'
    with pytest.raises(ValueError): transition_record(RECORD,"impossible")
def test_domain_rule_rejects_invalid_value():
    invalid=dict(RECORD); invalid.update({"measured_error_microns": 9999})
    with pytest.raises(ValueError): validate_record(invalid)
def test_signature_roundtrip_and_tamper_rejection():
    private=generate_signer(); public=private.public_key(); signature=sign_record(RECORD,private)
    assert verify_record(RECORD,signature,public)
    altered=dict(RECORD); altered["record_id"]+="-changed"
    assert not verify_record(altered,signature,public)
    assert not verify_record(RECORD,signature,generate_signer().public_key())
    assert load_public_key(export_public_key(public)).public_bytes_raw()==export_public_key(public).split(b":",1)[-1] if True else load_public_key(export_public_key(public)).public_numbers()==public.public_numbers()
def test_artifact_envelope_integrity():
    if True:
        recipient=generate_recipient(); private=recipient; public=recipient.public_key()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        private=rsa.generate_private_key(public_exponent=65537,key_size=3072); public=private.public_key()
    envelope=seal_artifact(b"FixtureCalibrationDossier synthetic artifact",public)
    assert open_artifact(envelope,private)==b"FixtureCalibrationDossier synthetic artifact"
    obj=json.loads(envelope); obj["ct"]=obj["ct"][:-4]+("AAAA" if obj["ct"][-4:]!="AAAA" else "BBBB")
    with pytest.raises(ValueError): open_artifact(json.dumps(obj).encode(),private)
    if True:
        wrong=generate_recipient()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        wrong=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    with pytest.raises(ValueError): open_artifact(envelope,wrong)
def test_unknown_envelope_version_rejected():
    if True:
        private=generate_recipient()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        private=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    with pytest.raises(ValueError): open_artifact(b'{"v":2,"alg":"unknown"}',private)
def test_persistent_application_approval_and_stale_record_rejection(tmp_path):
    from migrated_reference.fixture_calibration_dossier_pqc.service import FixtureCalibrationDossierPQC
    app=FixtureCalibrationDossierPQC(tmp_path/"workflow.sqlite3")
    app.register(RECORD)
    signer=generate_signer()
    app.approve(RECORD["record_id"],signer)
    assert app.verify_approval(RECORD["record_id"],signer.public_key())
    moved=app.advance(RECORD["record_id"],'measured')
    assert moved["state"]!='scheduled'
    assert not app.verify_approval(RECORD["record_id"],signer.public_key())

def test_fixture_acceptance_enforces_tolerance_and_expiry(tmp_path):
    from fixture_calibration_dossier_pqc.service import FixtureCalibrationDossierPQC
    record=dict(RECORD,state='measured'); app=FixtureCalibrationDossierPQC(tmp_path/'fixture.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.accept_fixture_calibration(record['record_id'],40,100,200,signer.public_key())
    assert result['state']=='accepted'
    with __import__('sqlite3').connect(app.path) as db: evidence=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert 'tolerance_microns' in evidence and 'fixture_id' in evidence
def test_fixture_acceptance_rejects_out_of_tolerance_and_expired_certificate(tmp_path):
    from fixture_calibration_dossier_pqc.service import FixtureCalibrationDossierPQC
    record=dict(RECORD,state='measured'); app=FixtureCalibrationDossierPQC(tmp_path/'fixture.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(ValueError): app.accept_fixture_calibration(record['record_id'],10,100,200,signer.public_key())
    with pytest.raises(ValueError): app.accept_fixture_calibration(record['record_id'],40,200,200,signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='measured'
