"""Application and crypto tests for ComponentTraceLot."""
import json, pytest
from component_trace_lot.domain import validate_record, canonical_record, transition_record
from component_trace_lot.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, seal_artifact, open_artifact

RECORD={"record_id": "trace-250", "component_id": "bearing-22", "source_lot": "mill-19-lot-5", "material_digest": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd", "receipt_sequence": 19, "state": "received"}
def test_domain_record_and_lifecycle():
    assert validate_record(RECORD)==RECORD
    assert canonical_record(RECORD)==canonical_record(dict(RECORD))
    changed=transition_record(RECORD,'verified')
    assert changed["state"]!='received'
    with pytest.raises(ValueError): transition_record(RECORD,"impossible")
def test_domain_rule_rejects_invalid_value():
    invalid=dict(RECORD); invalid.update({"material_digest": "short"})
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
    envelope=seal_artifact(b"ComponentTraceLot synthetic artifact",public)
    assert open_artifact(envelope,private)==b"ComponentTraceLot synthetic artifact"
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
    from component_trace_lot.service import ComponentTraceLot
    app=ComponentTraceLot(tmp_path/"workflow.sqlite3")
    app.register(RECORD)
    signer=generate_signer()
    app.approve(RECORD["record_id"],signer)
    assert app.verify_approval(RECORD["record_id"],signer.public_key())
    moved=app.advance(RECORD["record_id"],'verified')
    assert moved["state"]!='received'
    assert not app.verify_approval(RECORD["record_id"],signer.public_key())

def test_component_lot_consumption_checks_provenance_and_sequence(tmp_path):
    from component_trace_lot.service import ComponentTraceLot
    record=dict(RECORD,state='verified'); app=ComponentTraceLot(tmp_path/'trace.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.consume_component_lot(record['record_id'],record['receipt_sequence'],{record['material_digest']},signer.public_key())
    assert result['state']=='consumed'
    with __import__('sqlite3').connect(app.path) as db: ev=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert record['source_lot'] in ev and record['material_digest'] in ev
def test_component_lot_rejects_unapproved_digest_and_sequence(tmp_path):
    from component_trace_lot.service import ComponentTraceLot
    record=dict(RECORD,state='verified'); app=ComponentTraceLot(tmp_path/'trace.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.consume_component_lot(record['record_id'],record['receipt_sequence'],set(),signer.public_key())
    with pytest.raises(ValueError): app.consume_component_lot(record['record_id'],record['receipt_sequence']+1,{record['material_digest']},signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='verified'
