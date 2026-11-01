import json,pytest
from vendor_order.service import build_purchase_order,generate_purchase_order_signing_keypair,sign_purchase_order_decision,verify_purchase_order_decision,generate_purchase_order_recipient_keypair,seal_purchase_order_attachment,open_purchase_order_attachment,encode_purchase_order_recipient_public,load_purchase_order_recipient_public,rotate_purchase_order_attachment,validate_purchase_order_transition

SAMPLE={"order_id":"order-040","buyer_id":"buyer-1","supplier_id":"supplier-9","currency":"USD","total_cents":24500,"created_at":1800000000,"status":"draft"}
NEXT={"order_id":"order-040","buyer_id":"buyer-1","supplier_id":"supplier-9","currency":"USD","total_cents":24500,"created_at":1800000000,"status":"submitted"}
INVALID={"order_id":"order-040","buyer_id":"buyer-1","supplier_id":"supplier-9","currency":"USD","total_cents":0,"created_at":1800000000,"status":"draft"}

def test_vendor_order_business_validation_and_transition():
    record=build_purchase_order(SAMPLE); proposed=build_purchase_order(NEXT)
    assert validate_purchase_order_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["order_id"]="different-id"
    assert not validate_purchase_order_transition(json_bytes(record),json_bytes(build_purchase_order(changed)))
    assert not validate_purchase_order_transition(json_bytes(record),json_bytes(build_purchase_order(dict(SAMPLE))))
    with pytest.raises(ValueError): build_purchase_order({})
    with pytest.raises(ValueError): build_purchase_order(INVALID)

def test_vendor_order_signature_tamper_rejection():
    private,public=generate_purchase_order_signing_keypair(); record=build_purchase_order(SAMPLE); signature=sign_purchase_order_decision(record,private)
    assert verify_purchase_order_decision(record,signature,public)
    changed=dict(record); changed["order_id"]+="-changed"
    assert not verify_purchase_order_decision(changed,signature,public)

def test_vendor_order_attachment_context_and_authentication():
    private,public=generate_purchase_order_recipient_keypair(); env=seal_purchase_order_attachment(b"synthetic evidence",public,"order-040")
    assert open_purchase_order_attachment(env,private,"order-040")==b"synthetic evidence"
    with pytest.raises(ValueError): open_purchase_order_attachment(env,private,"wrong-id")
    other,_=generate_purchase_order_recipient_keypair()
    with pytest.raises(ValueError): open_purchase_order_attachment(env,other,"order-040")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_purchase_order_attachment(bytes(damaged),private,"order-040")

def test_vendor_order_recipient_encoding_and_rotation():
    old,old_public=generate_purchase_order_recipient_keypair(); new,new_public=generate_purchase_order_recipient_keypair()
    env=seal_purchase_order_attachment(b"rotation fixture",old_public,"order-040")
    rotated=rotate_purchase_order_attachment(env,old,new_public,"order-040")
    assert open_purchase_order_attachment(rotated,new,"order-040")==b"rotation fixture"
    encoded=encode_purchase_order_recipient_public(new_public)
    loaded=load_purchase_order_recipient_public(encoded)
    assert encode_purchase_order_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
