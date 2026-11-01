import json,pytest
from sbom_sign.service import build_sbom_release,generate_sbom_release_signing_keypair,sign_sbom_release_decision,verify_sbom_release_decision,generate_sbom_release_recipient_keypair,seal_sbom_release_attachment,open_sbom_release_attachment,encode_sbom_release_recipient_public,load_sbom_release_recipient_public,rotate_sbom_release_attachment,validate_sbom_release_transition

SAMPLE={"bom_id":"bom-046","artifact_digest":"3333333333333333333333333333333333333333333333333333333333333333","supplier_id":"supplier-46","serial_format":"SPDX-2.3","created_at":1800000000,"verification_state":"draft"}
NEXT={"bom_id":"bom-046","artifact_digest":"3333333333333333333333333333333333333333333333333333333333333333","supplier_id":"supplier-46","serial_format":"SPDX-2.3","created_at":1800000000,"verification_state":"signed"}
INVALID={"bom_id":"bom-046","artifact_digest":"3333333333333333333333333333333333333333333333333333333333333333","supplier_id":"supplier-46","serial_format":"unknown","created_at":1800000000,"verification_state":"draft"}

def test_sbom_sign_business_validation_and_transition():
    record=build_sbom_release(SAMPLE); proposed=build_sbom_release(NEXT)
    assert validate_sbom_release_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["bom_id"]="different-id"
    assert not validate_sbom_release_transition(json_bytes(record),json_bytes(build_sbom_release(changed)))
    assert not validate_sbom_release_transition(json_bytes(record),json_bytes(build_sbom_release(dict(SAMPLE))))
    with pytest.raises(ValueError): build_sbom_release({})
    with pytest.raises(ValueError): build_sbom_release(INVALID)

def test_sbom_sign_signature_tamper_rejection():
    private,public=generate_sbom_release_signing_keypair(); record=build_sbom_release(SAMPLE); signature=sign_sbom_release_decision(record,private)
    assert verify_sbom_release_decision(record,signature,public)
    changed=dict(record); changed["bom_id"]+="-changed"
    assert not verify_sbom_release_decision(changed,signature,public)

def test_sbom_sign_attachment_context_and_authentication():
    private,public=generate_sbom_release_recipient_keypair(); env=seal_sbom_release_attachment(b"synthetic evidence",public,"bom-046")
    assert open_sbom_release_attachment(env,private,"bom-046")==b"synthetic evidence"
    with pytest.raises(ValueError): open_sbom_release_attachment(env,private,"wrong-id")
    other,_=generate_sbom_release_recipient_keypair()
    with pytest.raises(ValueError): open_sbom_release_attachment(env,other,"bom-046")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_sbom_release_attachment(bytes(damaged),private,"bom-046")

def test_sbom_sign_recipient_encoding_and_rotation():
    old,old_public=generate_sbom_release_recipient_keypair(); new,new_public=generate_sbom_release_recipient_keypair()
    env=seal_sbom_release_attachment(b"rotation fixture",old_public,"bom-046")
    rotated=rotate_sbom_release_attachment(env,old,new_public,"bom-046")
    assert open_sbom_release_attachment(rotated,new,"bom-046")==b"rotation fixture"
    encoded=encode_sbom_release_recipient_public(new_public)
    loaded=load_sbom_release_recipient_public(encoded)
    assert encode_sbom_release_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
