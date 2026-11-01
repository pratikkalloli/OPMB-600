"""Application and crypto tests for ProductionDeviationCase."""
import json, pytest
from production_deviation_case.domain import validate_record, canonical_record, transition_record
from production_deviation_case.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, seal_artifact, open_artifact

RECORD={"record_id": "dev-248", "production_order": "po-551", "severity": "major", "nonconformance_code": "NC-17", "reporter_id": "inspector-4", "state": "opened"}
def test_domain_record_and_lifecycle():
    assert validate_record(RECORD)==RECORD
    assert canonical_record(RECORD)==canonical_record(dict(RECORD))
    changed=transition_record(RECORD,'contained')
    assert changed["state"]!='opened'
    with pytest.raises(ValueError): transition_record(RECORD,"impossible")
def test_domain_rule_rejects_invalid_value():
    invalid=dict(RECORD); invalid.update({"severity": "unknown"})
    with pytest.raises(ValueError): validate_record(invalid)
def test_signature_roundtrip_and_tamper_rejection():
    private=generate_signer(); public=private.public_key(); signature=sign_record(RECORD,private)
    assert verify_record(RECORD,signature,public)
    altered=dict(RECORD); altered["record_id"]+="-changed"
    assert not verify_record(altered,signature,public)
    assert not verify_record(RECORD,signature,generate_signer().public_key())
    assert load_public_key(export_public_key(public)).public_bytes_raw()==export_public_key(public).split(b":",1)[-1] if False else load_public_key(export_public_key(public)).public_numbers()==public.public_numbers()
def test_artifact_envelope_integrity():
    if False:
        recipient=generate_recipient(); private=recipient; public=recipient.public_key()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        private=rsa.generate_private_key(public_exponent=65537,key_size=3072); public=private.public_key()
    envelope=seal_artifact(b"ProductionDeviationCase synthetic artifact",public)
    assert open_artifact(envelope,private)==b"ProductionDeviationCase synthetic artifact"
    obj=json.loads(envelope); obj["ct"]=obj["ct"][:-4]+("AAAA" if obj["ct"][-4:]!="AAAA" else "BBBB")
    with pytest.raises(ValueError): open_artifact(json.dumps(obj).encode(),private)
    if False:
        wrong=generate_recipient()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        wrong=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    with pytest.raises(ValueError): open_artifact(envelope,wrong)
def test_unknown_envelope_version_rejected():
    if False:
        private=generate_recipient()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        private=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    with pytest.raises(ValueError): open_artifact(b'{"v":2,"alg":"unknown"}',private)
def test_persistent_application_approval_and_stale_record_rejection(tmp_path):
    from production_deviation_case.service import ProductionDeviationCase
    app=ProductionDeviationCase(tmp_path/"workflow.sqlite3")
    app.register(RECORD)
    signer=generate_signer()
    app.approve(RECORD["record_id"],signer)
    assert app.verify_approval(RECORD["record_id"],signer.public_key())
    moved=app.advance(RECORD["record_id"],'contained')
    assert moved["state"]!='opened'
    assert not app.verify_approval(RECORD["record_id"],signer.public_key())

def test_deviation_disposition_requires_independent_approval(tmp_path):
    from production_deviation_case.service import ProductionDeviationCase
    record=dict(RECORD,state='contained'); app=ProductionDeviationCase(tmp_path/'deviation.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.dispose_production_deviation(record['record_id'],'rework','quality-lead-2',signer.public_key())
    assert result['state']=='dispositioned'
    with __import__('sqlite3').connect(app.path) as db: ev=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert 'quality_manager_id' in ev and 'disposition' in ev
def test_deviation_rejects_reporter_self_approval_and_bad_disposition(tmp_path):
    from production_deviation_case.service import ProductionDeviationCase
    record=dict(RECORD,state='contained'); app=ProductionDeviationCase(tmp_path/'deviation.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.dispose_production_deviation(record['record_id'],'scrap',record['reporter_id'],signer.public_key())
    with pytest.raises(ValueError): app.dispose_production_deviation(record['record_id'],'unknown','quality-lead-2',signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='contained'
