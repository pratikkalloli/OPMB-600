import json,pytest
from key_recovery_pqc.service import build_recovery_case,generate_recovery_case_signing_keypair,sign_recovery_case_decision,verify_recovery_case_decision,generate_recovery_case_recipient_keypair,seal_recovery_case_attachment,open_recovery_case_attachment,encode_recovery_case_recipient_public,load_recovery_case_recipient_public,rotate_recovery_case_attachment,validate_recovery_case_transition

SAMPLE={"recovery_id":"recovery-044","principal_id":"principal-4","key_fingerprint":"2222222222222222222222222222222222222222222222222222222222222222","approvals_required":2,"opened_at":1800000000,"recovery_state":"opened"}
NEXT={"recovery_id":"recovery-044","principal_id":"principal-4","key_fingerprint":"2222222222222222222222222222222222222222222222222222222222222222","approvals_required":2,"opened_at":1800000000,"recovery_state":"approved"}
INVALID={"recovery_id":"recovery-044","principal_id":"principal-4","key_fingerprint":"2222222222222222222222222222222222222222222222222222222222222222","approvals_required":1,"opened_at":1800000000,"recovery_state":"opened"}

def test_key_recovery_business_validation_and_transition():
    record=build_recovery_case(SAMPLE); proposed=build_recovery_case(NEXT)
    assert validate_recovery_case_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["recovery_id"]="different-id"
    assert not validate_recovery_case_transition(json_bytes(record),json_bytes(build_recovery_case(changed)))
    assert not validate_recovery_case_transition(json_bytes(record),json_bytes(build_recovery_case(dict(SAMPLE))))
    with pytest.raises(ValueError): build_recovery_case({})
    with pytest.raises(ValueError): build_recovery_case(INVALID)

def test_key_recovery_signature_tamper_rejection():
    private,public=generate_recovery_case_signing_keypair(); record=build_recovery_case(SAMPLE); signature=sign_recovery_case_decision(record,private)
    assert verify_recovery_case_decision(record,signature,public)
    changed=dict(record); changed["recovery_id"]+="-changed"
    assert not verify_recovery_case_decision(changed,signature,public)

def test_key_recovery_attachment_context_and_authentication():
    private,public=generate_recovery_case_recipient_keypair(); env=seal_recovery_case_attachment(b"synthetic evidence",public,"recovery-044")
    assert open_recovery_case_attachment(env,private,"recovery-044")==b"synthetic evidence"
    with pytest.raises(ValueError): open_recovery_case_attachment(env,private,"wrong-id")
    other,_=generate_recovery_case_recipient_keypair()
    with pytest.raises(ValueError): open_recovery_case_attachment(env,other,"recovery-044")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_recovery_case_attachment(bytes(damaged),private,"recovery-044")

def test_key_recovery_recipient_encoding_and_rotation():
    old,old_public=generate_recovery_case_recipient_keypair(); new,new_public=generate_recovery_case_recipient_keypair()
    env=seal_recovery_case_attachment(b"rotation fixture",old_public,"recovery-044")
    rotated=rotate_recovery_case_attachment(env,old,new_public,"recovery-044")
    assert open_recovery_case_attachment(rotated,new,"recovery-044")==b"rotation fixture"
    encoded=encode_recovery_case_recipient_public(new_public)
    loaded=load_recovery_case_recipient_public(encoded)
    assert encode_recovery_case_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
