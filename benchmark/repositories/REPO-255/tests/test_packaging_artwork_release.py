"""Application and crypto tests for PackagingArtworkRelease."""
import json, pytest
from packaging_artwork_release.domain import validate_record, canonical_record, transition_record
from packaging_artwork_release.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, seal_artifact, open_artifact

RECORD={"record_id": "packaging_artwork_release-255", "workcell_id": "workcell-255", "review_class": "major", "event_code": "EVT-255", "sequence": 255, "state": "draft"}
def test_domain_record_and_lifecycle():
    assert validate_record(RECORD)==RECORD
    assert canonical_record(RECORD)==canonical_record(dict(RECORD))
    changed=transition_record(RECORD,'reviewed')
    assert changed["state"]!='draft'
    with pytest.raises(ValueError): transition_record(RECORD,"impossible")
def test_domain_rule_rejects_invalid_value():
    invalid=dict(RECORD); invalid.update({"review_class": "unknown"})
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
    envelope=seal_artifact(b"PackagingArtworkRelease synthetic artifact",public)
    assert open_artifact(envelope,private)==b"PackagingArtworkRelease synthetic artifact"
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
    from packaging_artwork_release.service import PackagingArtworkRelease
    app=PackagingArtworkRelease(tmp_path/"workflow.sqlite3")
    app.register(RECORD)
    signer=generate_signer()
    app.approve(RECORD["record_id"],signer)
    assert app.verify_approval(RECORD["record_id"],signer.public_key())
    moved=app.advance(RECORD["record_id"],'reviewed')
    assert moved["state"]!='draft'
    assert not app.verify_approval(RECORD["record_id"],signer.public_key())

def test_release_packaging_artwork_enforces_packaging_artwork_release_policy(tmp_path):
    from packaging_artwork_release.service import PackagingArtworkRelease
    record=dict(RECORD,state='reviewed'); app=PackagingArtworkRelease(tmp_path/'domain.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.release_packaging_artwork(record['record_id'], revision='ART-255-R2', approved_revisions={'ART-255-R2'}, market='US', authorized_markets={'US', 'CA'}, artwork_digest='a'*64, regulatory_clearance=True, release_public=signer.public_key())
    assert result['state']=='released'
    with __import__('sqlite3').connect(app.path) as db:
        event=db.execute('SELECT event_type,previous_state,next_state FROM workflow_events').fetchone()
    assert event[0] and event[1:] == ('reviewed','released')

def test_release_packaging_artwork_rejects_packaging_artwork_release_policy_violation_without_transition(tmp_path):
    from packaging_artwork_release.service import PackagingArtworkRelease
    record=dict(RECORD,state='reviewed'); app=PackagingArtworkRelease(tmp_path/'domain.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises((ValueError,PermissionError)):
        app.release_packaging_artwork(record['record_id'], revision='ART-255-R1', approved_revisions={'ART-255-R2'}, market='US', authorized_markets={'US'}, artwork_digest='a'*64, regulatory_clearance=True, release_public=signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='reviewed'
