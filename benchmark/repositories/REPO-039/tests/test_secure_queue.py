import json,pytest
from secure_queue.service import build_queue_message,generate_queue_message_signing_keypair,sign_queue_message_decision,verify_queue_message_decision,generate_queue_message_recipient_keypair,seal_queue_message_attachment,open_queue_message_attachment,encode_queue_message_recipient_public,load_queue_message_recipient_public,rotate_queue_message_attachment,validate_queue_message_transition

SAMPLE={"message_id":"msg-039","queue_name":"billing-events","producer_id":"svc-billing","created_at":1800000000,"expires_at":1800003600,"delivery_state":"pending"}
NEXT={"message_id":"msg-039","queue_name":"billing-events","producer_id":"svc-billing","created_at":1800000000,"expires_at":1800003600,"delivery_state":"leased"}
INVALID={"message_id":"msg-039","queue_name":"billing-events","producer_id":"svc-billing","created_at":1800000000,"expires_at":1800000000,"delivery_state":"pending"}

def test_secure_queue_business_validation_and_transition():
    record=build_queue_message(SAMPLE); proposed=build_queue_message(NEXT)
    assert validate_queue_message_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["message_id"]="different-id"
    assert not validate_queue_message_transition(json_bytes(record),json_bytes(build_queue_message(changed)))
    assert not validate_queue_message_transition(json_bytes(record),json_bytes(build_queue_message(dict(SAMPLE))))
    with pytest.raises(ValueError): build_queue_message({})
    with pytest.raises(ValueError): build_queue_message(INVALID)

def test_secure_queue_signature_tamper_rejection():
    private,public=generate_queue_message_signing_keypair(); record=build_queue_message(SAMPLE); signature=sign_queue_message_decision(record,private)
    assert verify_queue_message_decision(record,signature,public)
    changed=dict(record); changed["message_id"]+="-changed"
    assert not verify_queue_message_decision(changed,signature,public)

def test_secure_queue_attachment_context_and_authentication():
    private,public=generate_queue_message_recipient_keypair(); env=seal_queue_message_attachment(b"synthetic evidence",public,"msg-039")
    assert open_queue_message_attachment(env,private,"msg-039")==b"synthetic evidence"
    with pytest.raises(ValueError): open_queue_message_attachment(env,private,"wrong-id")
    other,_=generate_queue_message_recipient_keypair()
    with pytest.raises(ValueError): open_queue_message_attachment(env,other,"msg-039")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_queue_message_attachment(bytes(damaged),private,"msg-039")

def test_secure_queue_recipient_encoding_and_rotation():
    old,old_public=generate_queue_message_recipient_keypair(); new,new_public=generate_queue_message_recipient_keypair()
    env=seal_queue_message_attachment(b"rotation fixture",old_public,"msg-039")
    rotated=rotate_queue_message_attachment(env,old,new_public,"msg-039")
    assert open_queue_message_attachment(rotated,new,"msg-039")==b"rotation fixture"
    encoded=encode_queue_message_recipient_public(new_public)
    loaded=load_queue_message_recipient_public(encoded)
    assert encode_queue_message_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
