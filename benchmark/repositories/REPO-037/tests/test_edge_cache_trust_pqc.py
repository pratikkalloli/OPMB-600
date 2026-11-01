import json,pytest
from edge_cache_trust_pqc.service import build_cache_lease,generate_cache_lease_signing_keypair,sign_cache_lease_decision,verify_cache_lease_decision,generate_cache_lease_recipient_keypair,seal_cache_lease_attachment,open_cache_lease_attachment,encode_cache_lease_recipient_public,load_cache_lease_recipient_public,rotate_cache_lease_attachment,validate_cache_lease_transition

SAMPLE={"lease_id":"lease-037","object_key":"catalog/item-8","origin_digest":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","etag":"etag-8","fresh_until":1800000300,"trust_tier":"origin-verified","state":"fresh"}
NEXT={"lease_id":"lease-037","object_key":"catalog/item-8","origin_digest":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","etag":"etag-8","fresh_until":1800000300,"trust_tier":"origin-verified","state":"stale"}
INVALID={"lease_id":"lease-037","object_key":"catalog/item-8","origin_digest":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","etag":"etag-8","fresh_until":1800000300,"trust_tier":"unknown","state":"fresh"}

def test_edge_cache_trust_business_validation_and_transition():
    record=build_cache_lease(SAMPLE); proposed=build_cache_lease(NEXT)
    assert validate_cache_lease_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["lease_id"]="different-id"
    assert not validate_cache_lease_transition(json_bytes(record),json_bytes(build_cache_lease(changed)))
    assert not validate_cache_lease_transition(json_bytes(record),json_bytes(build_cache_lease(dict(SAMPLE))))
    with pytest.raises(ValueError): build_cache_lease({})
    with pytest.raises(ValueError): build_cache_lease(INVALID)

def test_edge_cache_trust_signature_tamper_rejection():
    private,public=generate_cache_lease_signing_keypair(); record=build_cache_lease(SAMPLE); signature=sign_cache_lease_decision(record,private)
    assert verify_cache_lease_decision(record,signature,public)
    changed=dict(record); changed["lease_id"]+="-changed"
    assert not verify_cache_lease_decision(changed,signature,public)

def test_edge_cache_trust_attachment_context_and_authentication():
    private,public=generate_cache_lease_recipient_keypair(); env=seal_cache_lease_attachment(b"synthetic evidence",public,"lease-037")
    assert open_cache_lease_attachment(env,private,"lease-037")==b"synthetic evidence"
    with pytest.raises(ValueError): open_cache_lease_attachment(env,private,"wrong-id")
    other,_=generate_cache_lease_recipient_keypair()
    with pytest.raises(ValueError): open_cache_lease_attachment(env,other,"lease-037")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_cache_lease_attachment(bytes(damaged),private,"lease-037")

def test_edge_cache_trust_recipient_encoding_and_rotation():
    old,old_public=generate_cache_lease_recipient_keypair(); new,new_public=generate_cache_lease_recipient_keypair()
    env=seal_cache_lease_attachment(b"rotation fixture",old_public,"lease-037")
    rotated=rotate_cache_lease_attachment(env,old,new_public,"lease-037")
    assert open_cache_lease_attachment(rotated,new,"lease-037")==b"rotation fixture"
    encoded=encode_cache_lease_recipient_public(new_public)
    loaded=load_cache_lease_recipient_public(encoded)
    assert encode_cache_lease_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
