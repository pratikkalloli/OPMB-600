import json,pytest
from research_release_pqc.service import build_dataset_release,generate_dataset_release_signing_keypair,sign_dataset_release_decision,verify_dataset_release_decision,generate_dataset_release_recipient_keypair,seal_dataset_release_attachment,open_dataset_release_attachment,encode_dataset_release_recipient_public,load_dataset_release_recipient_public,rotate_dataset_release_attachment,validate_dataset_release_transition

SAMPLE={"release_id":"release-038","dataset_digest":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd","curator_id":"curator-3","license_id":"CC-BY-4.0","embargo_until":1800000000,"status":"draft"}
NEXT={"release_id":"release-038","dataset_digest":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd","curator_id":"curator-3","license_id":"CC-BY-4.0","embargo_until":1800000000,"status":"approved"}
INVALID={"release_id":"release-038","dataset_digest":"bad","curator_id":"curator-3","license_id":"CC-BY-4.0","embargo_until":1800000000,"status":"draft"}

def test_research_release_business_validation_and_transition():
    record=build_dataset_release(SAMPLE); proposed=build_dataset_release(NEXT)
    assert validate_dataset_release_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["release_id"]="different-id"
    assert not validate_dataset_release_transition(json_bytes(record),json_bytes(build_dataset_release(changed)))
    assert not validate_dataset_release_transition(json_bytes(record),json_bytes(build_dataset_release(dict(SAMPLE))))
    with pytest.raises(ValueError): build_dataset_release({})
    with pytest.raises(ValueError): build_dataset_release(INVALID)

def test_research_release_signature_tamper_rejection():
    private,public=generate_dataset_release_signing_keypair(); record=build_dataset_release(SAMPLE); signature=sign_dataset_release_decision(record,private)
    assert verify_dataset_release_decision(record,signature,public)
    changed=dict(record); changed["release_id"]+="-changed"
    assert not verify_dataset_release_decision(changed,signature,public)

def test_research_release_attachment_context_and_authentication():
    private,public=generate_dataset_release_recipient_keypair(); env=seal_dataset_release_attachment(b"synthetic evidence",public,"release-038")
    assert open_dataset_release_attachment(env,private,"release-038")==b"synthetic evidence"
    with pytest.raises(ValueError): open_dataset_release_attachment(env,private,"wrong-id")
    other,_=generate_dataset_release_recipient_keypair()
    with pytest.raises(ValueError): open_dataset_release_attachment(env,other,"release-038")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_dataset_release_attachment(bytes(damaged),private,"release-038")

def test_research_release_recipient_encoding_and_rotation():
    old,old_public=generate_dataset_release_recipient_keypair(); new,new_public=generate_dataset_release_recipient_keypair()
    env=seal_dataset_release_attachment(b"rotation fixture",old_public,"release-038")
    rotated=rotate_dataset_release_attachment(env,old,new_public,"release-038")
    assert open_dataset_release_attachment(rotated,new,"release-038")==b"rotation fixture"
    encoded=encode_dataset_release_recipient_public(new_public)
    loaded=load_dataset_release_recipient_public(encoded)
    assert encode_dataset_release_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
