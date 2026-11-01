import json,pytest
from tenant_portal.service import build_tenant_invitation,generate_tenant_invitation_signing_keypair,sign_tenant_invitation_decision,verify_tenant_invitation_decision,generate_tenant_invitation_recipient_keypair,seal_tenant_invitation_attachment,open_tenant_invitation_attachment,encode_tenant_invitation_recipient_public,load_tenant_invitation_recipient_public,rotate_tenant_invitation_attachment,validate_tenant_invitation_transition

SAMPLE={"invitation_id":"inv-033","tenant_id":"tenant-7","invitee_email":"person@example.invalid","role":"viewer","expires_at":1900000000,"status":"pending"}
NEXT={"invitation_id":"inv-033","tenant_id":"tenant-7","invitee_email":"person@example.invalid","role":"viewer","expires_at":1900000000,"status":"accepted"}
INVALID={"invitation_id":"inv-033","tenant_id":"tenant-7","invitee_email":"person@example.invalid","role":"unknown","expires_at":1900000000,"status":"pending"}

def test_tenant_portal_business_validation_and_transition():
    record=build_tenant_invitation(SAMPLE); proposed=build_tenant_invitation(NEXT)
    assert validate_tenant_invitation_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["invitation_id"]="different-id"
    assert not validate_tenant_invitation_transition(json_bytes(record),json_bytes(build_tenant_invitation(changed)))
    assert not validate_tenant_invitation_transition(json_bytes(record),json_bytes(build_tenant_invitation(dict(SAMPLE))))
    with pytest.raises(ValueError): build_tenant_invitation({})
    with pytest.raises(ValueError): build_tenant_invitation(INVALID)

def test_tenant_portal_signature_tamper_rejection():
    private,public=generate_tenant_invitation_signing_keypair(); record=build_tenant_invitation(SAMPLE); signature=sign_tenant_invitation_decision(record,private)
    assert verify_tenant_invitation_decision(record,signature,public)
    changed=dict(record); changed["invitation_id"]+="-changed"
    assert not verify_tenant_invitation_decision(changed,signature,public)

def test_tenant_portal_attachment_context_and_authentication():
    private,public=generate_tenant_invitation_recipient_keypair(); env=seal_tenant_invitation_attachment(b"synthetic evidence",public,"inv-033")
    assert open_tenant_invitation_attachment(env,private,"inv-033")==b"synthetic evidence"
    with pytest.raises(ValueError): open_tenant_invitation_attachment(env,private,"wrong-id")
    other,_=generate_tenant_invitation_recipient_keypair()
    with pytest.raises(ValueError): open_tenant_invitation_attachment(env,other,"inv-033")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_tenant_invitation_attachment(bytes(damaged),private,"inv-033")

def test_tenant_portal_recipient_encoding_and_rotation():
    old,old_public=generate_tenant_invitation_recipient_keypair(); new,new_public=generate_tenant_invitation_recipient_keypair()
    env=seal_tenant_invitation_attachment(b"rotation fixture",old_public,"inv-033")
    rotated=rotate_tenant_invitation_attachment(env,old,new_public,"inv-033")
    assert open_tenant_invitation_attachment(rotated,new,"inv-033")==b"rotation fixture"
    encoded=encode_tenant_invitation_recipient_public(new_public)
    loaded=load_tenant_invitation_recipient_public(encoded)
    assert encode_tenant_invitation_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
