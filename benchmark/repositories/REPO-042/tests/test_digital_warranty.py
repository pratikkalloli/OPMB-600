import json,pytest
from digital_warranty.service import build_warranty_claim,generate_warranty_claim_signing_keypair,sign_warranty_claim_decision,verify_warranty_claim_decision,generate_warranty_claim_recipient_keypair,seal_warranty_claim_attachment,open_warranty_claim_attachment,encode_warranty_claim_recipient_public,load_warranty_claim_recipient_public,rotate_warranty_claim_attachment,validate_warranty_claim_transition

SAMPLE={"claim_id":"claim-042","product_serial":"SN-42-A","claimant_id":"customer-6","evidence_digest":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","submitted_at":1800000000,"status":"submitted"}
NEXT={"claim_id":"claim-042","product_serial":"SN-42-A","claimant_id":"customer-6","evidence_digest":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","submitted_at":1800000000,"status":"reviewing"}
INVALID={"claim_id":"claim-042","product_serial":"SN-42-A","claimant_id":"customer-6","evidence_digest":"bad","submitted_at":1800000000,"status":"submitted"}

def test_digital_warranty_business_validation_and_transition():
    record=build_warranty_claim(SAMPLE); proposed=build_warranty_claim(NEXT)
    assert validate_warranty_claim_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["claim_id"]="different-id"
    assert not validate_warranty_claim_transition(json_bytes(record),json_bytes(build_warranty_claim(changed)))
    assert not validate_warranty_claim_transition(json_bytes(record),json_bytes(build_warranty_claim(dict(SAMPLE))))
    with pytest.raises(ValueError): build_warranty_claim({})
    with pytest.raises(ValueError): build_warranty_claim(INVALID)

def test_digital_warranty_signature_tamper_rejection():
    private,public=generate_warranty_claim_signing_keypair(); record=build_warranty_claim(SAMPLE); signature=sign_warranty_claim_decision(record,private)
    assert verify_warranty_claim_decision(record,signature,public)
    changed=dict(record); changed["claim_id"]+="-changed"
    assert not verify_warranty_claim_decision(changed,signature,public)

def test_digital_warranty_attachment_context_and_authentication():
    private,public=generate_warranty_claim_recipient_keypair(); env=seal_warranty_claim_attachment(b"synthetic evidence",public,"claim-042")
    assert open_warranty_claim_attachment(env,private,"claim-042")==b"synthetic evidence"
    with pytest.raises(ValueError): open_warranty_claim_attachment(env,private,"wrong-id")
    other,_=generate_warranty_claim_recipient_keypair()
    with pytest.raises(ValueError): open_warranty_claim_attachment(env,other,"claim-042")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_warranty_claim_attachment(bytes(damaged),private,"claim-042")

def test_digital_warranty_recipient_encoding_and_rotation():
    old,old_public=generate_warranty_claim_recipient_keypair(); new,new_public=generate_warranty_claim_recipient_keypair()
    env=seal_warranty_claim_attachment(b"rotation fixture",old_public,"claim-042")
    rotated=rotate_warranty_claim_attachment(env,old,new_public,"claim-042")
    assert open_warranty_claim_attachment(rotated,new,"claim-042")==b"rotation fixture"
    encoded=encode_warranty_claim_recipient_public(new_public)
    loaded=load_warranty_claim_recipient_public(encoded)
    assert encode_warranty_claim_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
