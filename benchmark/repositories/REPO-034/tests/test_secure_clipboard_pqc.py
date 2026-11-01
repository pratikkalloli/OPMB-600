import json,pytest
from secure_clipboard_pqc.service import build_clipboard_share,generate_clipboard_share_signing_keypair,sign_clipboard_share_decision,verify_clipboard_share_decision,generate_clipboard_share_recipient_keypair,seal_clipboard_share_attachment,open_clipboard_share_attachment,encode_clipboard_share_recipient_public,load_clipboard_share_recipient_public,rotate_clipboard_share_attachment,validate_clipboard_share_transition

SAMPLE={"clip_id":"clip-034","owner_id":"user-a","recipient_id":"user-b","sensitivity":"confidential","created_at":1800000000,"expires_at":1800003600,"status":"active"}
NEXT={"clip_id":"clip-034","owner_id":"user-a","recipient_id":"user-b","sensitivity":"confidential","created_at":1800000000,"expires_at":1800003600,"status":"revoked"}
INVALID={"clip_id":"clip-034","owner_id":"user-a","recipient_id":"user-b","sensitivity":"confidential","created_at":1800000000,"expires_at":1800000000,"status":"active"}

def test_secure_clipboard_business_validation_and_transition():
    record=build_clipboard_share(SAMPLE); proposed=build_clipboard_share(NEXT)
    assert validate_clipboard_share_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["clip_id"]="different-id"
    assert not validate_clipboard_share_transition(json_bytes(record),json_bytes(build_clipboard_share(changed)))
    assert not validate_clipboard_share_transition(json_bytes(record),json_bytes(build_clipboard_share(dict(SAMPLE))))
    with pytest.raises(ValueError): build_clipboard_share({})
    with pytest.raises(ValueError): build_clipboard_share(INVALID)

def test_secure_clipboard_signature_tamper_rejection():
    private,public=generate_clipboard_share_signing_keypair(); record=build_clipboard_share(SAMPLE); signature=sign_clipboard_share_decision(record,private)
    assert verify_clipboard_share_decision(record,signature,public)
    changed=dict(record); changed["clip_id"]+="-changed"
    assert not verify_clipboard_share_decision(changed,signature,public)

def test_secure_clipboard_attachment_context_and_authentication():
    private,public=generate_clipboard_share_recipient_keypair(); env=seal_clipboard_share_attachment(b"synthetic evidence",public,"clip-034")
    assert open_clipboard_share_attachment(env,private,"clip-034")==b"synthetic evidence"
    with pytest.raises(ValueError): open_clipboard_share_attachment(env,private,"wrong-id")
    other,_=generate_clipboard_share_recipient_keypair()
    with pytest.raises(ValueError): open_clipboard_share_attachment(env,other,"clip-034")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_clipboard_share_attachment(bytes(damaged),private,"clip-034")

def test_secure_clipboard_recipient_encoding_and_rotation():
    old,old_public=generate_clipboard_share_recipient_keypair(); new,new_public=generate_clipboard_share_recipient_keypair()
    env=seal_clipboard_share_attachment(b"rotation fixture",old_public,"clip-034")
    rotated=rotate_clipboard_share_attachment(env,old,new_public,"clip-034")
    assert open_clipboard_share_attachment(rotated,new,"clip-034")==b"rotation fixture"
    encoded=encode_clipboard_share_recipient_public(new_public)
    loaded=load_clipboard_share_recipient_public(encoded)
    assert encode_clipboard_share_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
