"""Application and crypto tests for LineClearanceToken."""
import json, pytest
from line_clearance_token.domain import validate_record, canonical_record, transition_record
from line_clearance_token.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, seal_artifact, open_artifact

RECORD={"record_id": "clear-242", "line_id": "line-pack-2", "product_code": "SKU-88", "clearance_code": "CL-242-A", "shift_id": "shift-north", "state": "requested"}
def test_domain_record_and_lifecycle():
    assert validate_record(RECORD)==RECORD
    assert canonical_record(RECORD)==canonical_record(dict(RECORD))
    changed=transition_record(RECORD,'inspected')
    assert changed["state"]!='requested'
    with pytest.raises(ValueError): transition_record(RECORD,"impossible")
def test_domain_rule_rejects_invalid_value():
    invalid=dict(RECORD); invalid.update({"clearance_code": "bad code"})
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
    envelope=seal_artifact(b"LineClearanceToken synthetic artifact",public)
    assert open_artifact(envelope,private)==b"LineClearanceToken synthetic artifact"
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
    from line_clearance_token.service import LineClearanceToken
    app=LineClearanceToken(tmp_path/"workflow.sqlite3")
    app.register(RECORD)
    signer=generate_signer()
    app.approve(RECORD["record_id"],signer)
    assert app.verify_approval(RECORD["record_id"],signer.public_key())
    moved=app.advance(RECORD["record_id"],'inspected')
    assert moved["state"]!='requested'
    assert not app.verify_approval(RECORD["record_id"],signer.public_key())

def test_line_clearance_requires_shift_and_all_checks(tmp_path):
    from line_clearance_token.service import LineClearanceToken
    record=dict(RECORD,state='inspected'); app=LineClearanceToken(tmp_path/'line.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    checks={'guards_secured':True,'previous_product_removed':True,'tools_accounted':True}
    result=app.clear_production_line(record['record_id'],record['shift_id'],checks,signer.public_key())
    assert result['state']=='cleared'
    with __import__('sqlite3').connect(app.path) as db: assert db.execute('SELECT event_type FROM workflow_events').fetchone()[0]=='line_cleared'
def test_line_clearance_rejects_wrong_shift_or_incomplete_checklist(tmp_path):
    from line_clearance_token.service import LineClearanceToken
    record=dict(RECORD,state='inspected'); app=LineClearanceToken(tmp_path/'line.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.clear_production_line(record['record_id'],'another-shift',{'guards_secured':True,'previous_product_removed':True,'tools_accounted':True},signer.public_key())
    with pytest.raises(ValueError): app.clear_production_line(record['record_id'],record['shift_id'],{'guards_secured':True},signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='inspected'
