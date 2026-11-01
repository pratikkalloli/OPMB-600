import json,pytest
from redaction_proof.service import build_redaction_case,generate_redaction_case_signing_keypair,sign_redaction_case_decision,verify_redaction_case_decision,generate_redaction_case_recipient_keypair,seal_redaction_case_attachment,open_redaction_case_attachment,encode_redaction_case_recipient_public,load_redaction_case_recipient_public,rotate_redaction_case_attachment,validate_redaction_case_transition

SAMPLE={"case_id":"case-035","document_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","redaction_map_digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","reviewer_id":"reviewer-2","disclosure_policy":"minimum-necessary","status":"draft"}
NEXT={"case_id":"case-035","document_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","redaction_map_digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","reviewer_id":"reviewer-2","disclosure_policy":"minimum-necessary","status":"approved"}
INVALID={"case_id":"case-035","document_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","redaction_map_digest":"short","reviewer_id":"reviewer-2","disclosure_policy":"minimum-necessary","status":"draft"}

def test_redaction_proof_business_validation_and_transition():
    record=build_redaction_case(SAMPLE); proposed=build_redaction_case(NEXT)
    assert validate_redaction_case_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["case_id"]="different-id"
    assert not validate_redaction_case_transition(json_bytes(record),json_bytes(build_redaction_case(changed)))
    assert not validate_redaction_case_transition(json_bytes(record),json_bytes(build_redaction_case(dict(SAMPLE))))
    with pytest.raises(ValueError): build_redaction_case({})
    with pytest.raises(ValueError): build_redaction_case(INVALID)

def test_redaction_proof_signature_tamper_rejection():
    private,public=generate_redaction_case_signing_keypair(); record=build_redaction_case(SAMPLE); signature=sign_redaction_case_decision(record,private)
    assert verify_redaction_case_decision(record,signature,public)
    changed=dict(record); changed["case_id"]+="-changed"
    assert not verify_redaction_case_decision(changed,signature,public)

def test_redaction_proof_attachment_context_and_authentication():
    private,public=generate_redaction_case_recipient_keypair(); env=seal_redaction_case_attachment(b"synthetic evidence",public,"case-035")
    assert open_redaction_case_attachment(env,private,"case-035")==b"synthetic evidence"
    with pytest.raises(ValueError): open_redaction_case_attachment(env,private,"wrong-id")
    other,_=generate_redaction_case_recipient_keypair()
    with pytest.raises(ValueError): open_redaction_case_attachment(env,other,"case-035")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_redaction_case_attachment(bytes(damaged),private,"case-035")

def test_redaction_proof_recipient_encoding_and_rotation():
    old,old_public=generate_redaction_case_recipient_keypair(); new,new_public=generate_redaction_case_recipient_keypair()
    env=seal_redaction_case_attachment(b"rotation fixture",old_public,"case-035")
    rotated=rotate_redaction_case_attachment(env,old,new_public,"case-035")
    assert open_redaction_case_attachment(rotated,new,"case-035")==b"rotation fixture"
    encoded=encode_redaction_case_recipient_public(new_public)
    loaded=load_redaction_case_recipient_public(encoded)
    assert encode_redaction_case_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
