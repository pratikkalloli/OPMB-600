"""Application and crypto tests for AssemblySequencePermit."""
import json, pytest
from assembly_sequence_permit.domain import validate_record, canonical_record, transition_record
from assembly_sequence_permit.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, seal_artifact, open_artifact

RECORD={"record_id": "assembly_sequence_permit-260", "workcell_id": "workcell-260", "event_count": 4, "event_code": "EVT-260", "sequence": 260, "state": "draft"}
def test_domain_record_and_lifecycle():
    assert validate_record(RECORD)==RECORD
    assert canonical_record(RECORD)==canonical_record(dict(RECORD))
    changed=transition_record(RECORD,'reviewed')
    assert changed["state"]!='draft'
    with pytest.raises(ValueError): transition_record(RECORD,"impossible")
def test_domain_rule_rejects_invalid_value():
    invalid=dict(RECORD); invalid.update({"event_count": -1})
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
    envelope=seal_artifact(b"AssemblySequencePermit synthetic artifact",public)
    assert open_artifact(envelope,private)==b"AssemblySequencePermit synthetic artifact"
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
    from assembly_sequence_permit.service import AssemblySequencePermit
    app=AssemblySequencePermit(tmp_path/"workflow.sqlite3")
    app.register(RECORD)
    signer=generate_signer()
    app.approve(RECORD["record_id"],signer)
    assert app.verify_approval(RECORD["record_id"],signer.public_key())
    moved=app.advance(RECORD["record_id"],'reviewed')
    assert moved["state"]!='draft'
    assert not app.verify_approval(RECORD["record_id"],signer.public_key())

def test_authorize_assembly_operation_enforces_assembly_sequence_permit_policy(tmp_path):
    from assembly_sequence_permit.service import AssemblySequencePermit
    record=dict(RECORD,state='reviewed'); app=AssemblySequencePermit(tmp_path/'domain.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.authorize_assembly_operation(record['record_id'], required_operations={'frame-fit', 'torque-check'}, completed_operations=['frame-fit', 'torque-check', 'seal', 'inspection'], next_sequence=RECORD['sequence'] + 1, production_public=signer.public_key())
    assert result['state']=='released'
    with __import__('sqlite3').connect(app.path) as db:
        event=db.execute('SELECT event_type,previous_state,next_state FROM workflow_events').fetchone()
    assert event[0] and event[1:] == ('reviewed','released')

def test_authorize_assembly_operation_rejects_assembly_sequence_permit_policy_violation_without_transition(tmp_path):
    from assembly_sequence_permit.service import AssemblySequencePermit
    record=dict(RECORD,state='reviewed'); app=AssemblySequencePermit(tmp_path/'domain.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises((ValueError,PermissionError)):
        app.authorize_assembly_operation(record['record_id'], required_operations={'frame-fit', 'torque-check'}, completed_operations=['frame-fit'], next_sequence=RECORD['sequence'] + 1, production_public=signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='reviewed'
