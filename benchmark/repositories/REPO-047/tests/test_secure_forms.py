import json,pytest
from secure_forms.service import build_form_submission,generate_form_submission_signing_keypair,sign_form_submission_decision,verify_form_submission_decision,generate_form_submission_recipient_keypair,seal_form_submission_attachment,open_form_submission_attachment,encode_form_submission_recipient_public,load_form_submission_recipient_public,rotate_form_submission_attachment,validate_form_submission_transition

SAMPLE={"form_id":"form-047","submission_id":"submission-47","submitter_ref":"subject-47","schema_version":3,"received_at":1800000000,"consent_version":"consent-2026-1","processing_state":"received"}
NEXT={"form_id":"form-047","submission_id":"submission-47","submitter_ref":"subject-47","schema_version":3,"received_at":1800000000,"consent_version":"consent-2026-1","processing_state":"validated"}
INVALID={"form_id":"form-047","submission_id":"submission-47","submitter_ref":"subject-47","schema_version":0,"received_at":1800000000,"consent_version":"consent-2026-1","processing_state":"received"}

def test_secure_forms_business_validation_and_transition():
    record=build_form_submission(SAMPLE); proposed=build_form_submission(NEXT)
    assert validate_form_submission_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["form_id"]="different-id"
    assert not validate_form_submission_transition(json_bytes(record),json_bytes(build_form_submission(changed)))
    assert not validate_form_submission_transition(json_bytes(record),json_bytes(build_form_submission(dict(SAMPLE))))
    with pytest.raises(ValueError): build_form_submission({})
    with pytest.raises(ValueError): build_form_submission(INVALID)

def test_secure_forms_signature_tamper_rejection():
    private,public=generate_form_submission_signing_keypair(); record=build_form_submission(SAMPLE); signature=sign_form_submission_decision(record,private)
    assert verify_form_submission_decision(record,signature,public)
    changed=dict(record); changed["form_id"]+="-changed"
    assert not verify_form_submission_decision(changed,signature,public)

def test_secure_forms_attachment_context_and_authentication():
    private,public=generate_form_submission_recipient_keypair(); env=seal_form_submission_attachment(b"synthetic evidence",public,"form-047")
    assert open_form_submission_attachment(env,private,"form-047")==b"synthetic evidence"
    with pytest.raises(ValueError): open_form_submission_attachment(env,private,"wrong-id")
    other,_=generate_form_submission_recipient_keypair()
    with pytest.raises(ValueError): open_form_submission_attachment(env,other,"form-047")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_form_submission_attachment(bytes(damaged),private,"form-047")

def test_secure_forms_recipient_encoding_and_rotation():
    old,old_public=generate_form_submission_recipient_keypair(); new,new_public=generate_form_submission_recipient_keypair()
    env=seal_form_submission_attachment(b"rotation fixture",old_public,"form-047")
    rotated=rotate_form_submission_attachment(env,old,new_public,"form-047")
    assert open_form_submission_attachment(rotated,new,"form-047")==b"rotation fixture"
    encoded=encode_form_submission_recipient_public(new_public)
    loaded=load_form_submission_recipient_public(encoded)
    assert encode_form_submission_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
