"""Application and crypto tests for NetworkChangeWindow PQC reference."""
import json, pytest
from network_change_window_pqc.domain import validate_record, canonical_record, transition_record
from network_change_window_pqc.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, generate_recipient, seal_artifact, open_artifact

RECORD={"record_id": "network_change_window-373", "network_element_id": "network_element-373", "measured_value": 25, "event_code": "EVT-373", "sequence": 373, "state": "provisioned"}
def test_domain_record_and_lifecycle():
    assert validate_record(RECORD)==RECORD
    assert canonical_record(RECORD)==canonical_record(dict(RECORD))
    changed=transition_record(RECORD,'active')
    assert changed["state"]!='provisioned'
    with pytest.raises(ValueError): transition_record(RECORD,"impossible")
def test_domain_rule_rejects_invalid_value():
    invalid=dict(RECORD); invalid.update({"measured_value": 1001})
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
    envelope=seal_artifact(b"NetworkChangeWindow synthetic artifact",public)
    assert open_artifact(envelope,private)==b"NetworkChangeWindow synthetic artifact"
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
    from migrated_reference.network_change_window_pqc.service import NetworkChangeWindowPQC
    app=NetworkChangeWindowPQC(tmp_path/"workflow.sqlite3")
    app.register(RECORD)
    signer=generate_signer()
    app.approve(RECORD["record_id"],signer)
    assert app.verify_approval(RECORD["record_id"],signer.public_key())
    moved=app.advance(RECORD["record_id"],'active')
    assert moved["state"]!='provisioned'
    assert not app.verify_approval(RECORD["record_id"],signer.public_key())
