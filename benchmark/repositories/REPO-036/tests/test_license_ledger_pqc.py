import json,pytest
from license_ledger_pqc.service import build_license_record,generate_license_record_signing_keypair,sign_license_record_decision,verify_license_record_decision,generate_license_record_recipient_keypair,seal_license_record_attachment,open_license_record_attachment,encode_license_record_recipient_public,load_license_record_recipient_public,rotate_license_record_attachment,validate_license_record_transition

SAMPLE={"license_id":"lic-036","product_id":"editor","organization_id":"org-12","seat_count":25,"expires_at":1900000000,"status":"trial"}
NEXT={"license_id":"lic-036","product_id":"editor","organization_id":"org-12","seat_count":25,"expires_at":1900000000,"status":"active"}
INVALID={"license_id":"lic-036","product_id":"editor","organization_id":"org-12","seat_count":0,"expires_at":1900000000,"status":"trial"}

def test_license_ledger_business_validation_and_transition():
    record=build_license_record(SAMPLE); proposed=build_license_record(NEXT)
    assert validate_license_record_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["license_id"]="different-id"
    assert not validate_license_record_transition(json_bytes(record),json_bytes(build_license_record(changed)))
    assert not validate_license_record_transition(json_bytes(record),json_bytes(build_license_record(dict(SAMPLE))))
    with pytest.raises(ValueError): build_license_record({})
    with pytest.raises(ValueError): build_license_record(INVALID)

def test_license_ledger_signature_tamper_rejection():
    private,public=generate_license_record_signing_keypair(); record=build_license_record(SAMPLE); signature=sign_license_record_decision(record,private)
    assert verify_license_record_decision(record,signature,public)
    changed=dict(record); changed["license_id"]+="-changed"
    assert not verify_license_record_decision(changed,signature,public)

def test_license_ledger_attachment_context_and_authentication():
    private,public=generate_license_record_recipient_keypair(); env=seal_license_record_attachment(b"synthetic evidence",public,"lic-036")
    assert open_license_record_attachment(env,private,"lic-036")==b"synthetic evidence"
    with pytest.raises(ValueError): open_license_record_attachment(env,private,"wrong-id")
    other,_=generate_license_record_recipient_keypair()
    with pytest.raises(ValueError): open_license_record_attachment(env,other,"lic-036")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_license_record_attachment(bytes(damaged),private,"lic-036")

def test_license_ledger_recipient_encoding_and_rotation():
    old,old_public=generate_license_record_recipient_keypair(); new,new_public=generate_license_record_recipient_keypair()
    env=seal_license_record_attachment(b"rotation fixture",old_public,"lic-036")
    rotated=rotate_license_record_attachment(env,old,new_public,"lic-036")
    assert open_license_record_attachment(rotated,new,"lic-036")==b"rotation fixture"
    encoded=encode_license_record_recipient_public(new_public)
    loaded=load_license_record_recipient_public(encoded)
    assert encode_license_record_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
