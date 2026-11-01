import json,pytest
from photo_vault_pqc.service import build_photo_object,generate_photo_object_signing_keypair,sign_photo_object_decision,verify_photo_object_decision,generate_photo_object_recipient_keypair,seal_photo_object_attachment,open_photo_object_attachment,encode_photo_object_recipient_public,load_photo_object_recipient_public,rotate_photo_object_attachment,validate_photo_object_transition

SAMPLE={"photo_id":"photo-043","owner_id":"owner-43","content_digest":"1111111111111111111111111111111111111111111111111111111111111111","classification":"personal","retention_days":365,"lifecycle":"private"}
NEXT={"photo_id":"photo-043","owner_id":"owner-43","content_digest":"1111111111111111111111111111111111111111111111111111111111111111","classification":"personal","retention_days":365,"lifecycle":"shared"}
INVALID={"photo_id":"photo-043","owner_id":"owner-43","content_digest":"1111111111111111111111111111111111111111111111111111111111111111","classification":"personal","retention_days":0,"lifecycle":"private"}

def test_photo_vault_business_validation_and_transition():
    record=build_photo_object(SAMPLE); proposed=build_photo_object(NEXT)
    assert validate_photo_object_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["photo_id"]="different-id"
    assert not validate_photo_object_transition(json_bytes(record),json_bytes(build_photo_object(changed)))
    assert not validate_photo_object_transition(json_bytes(record),json_bytes(build_photo_object(dict(SAMPLE))))
    with pytest.raises(ValueError): build_photo_object({})
    with pytest.raises(ValueError): build_photo_object(INVALID)

def test_photo_vault_signature_tamper_rejection():
    private,public=generate_photo_object_signing_keypair(); record=build_photo_object(SAMPLE); signature=sign_photo_object_decision(record,private)
    assert verify_photo_object_decision(record,signature,public)
    changed=dict(record); changed["photo_id"]+="-changed"
    assert not verify_photo_object_decision(changed,signature,public)

def test_photo_vault_attachment_context_and_authentication():
    private,public=generate_photo_object_recipient_keypair(); env=seal_photo_object_attachment(b"synthetic evidence",public,"photo-043")
    assert open_photo_object_attachment(env,private,"photo-043")==b"synthetic evidence"
    with pytest.raises(ValueError): open_photo_object_attachment(env,private,"wrong-id")
    other,_=generate_photo_object_recipient_keypair()
    with pytest.raises(ValueError): open_photo_object_attachment(env,other,"photo-043")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_photo_object_attachment(bytes(damaged),private,"photo-043")

def test_photo_vault_recipient_encoding_and_rotation():
    old,old_public=generate_photo_object_recipient_keypair(); new,new_public=generate_photo_object_recipient_keypair()
    env=seal_photo_object_attachment(b"rotation fixture",old_public,"photo-043")
    rotated=rotate_photo_object_attachment(env,old,new_public,"photo-043")
    assert open_photo_object_attachment(rotated,new,"photo-043")==b"rotation fixture"
    encoded=encode_photo_object_recipient_public(new_public)
    loaded=load_photo_object_recipient_public(encoded)
    assert encode_photo_object_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
