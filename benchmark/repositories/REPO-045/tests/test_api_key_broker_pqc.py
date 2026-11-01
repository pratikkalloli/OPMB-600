import json,pytest
from api_key_broker_pqc.service import build_api_credential,generate_api_credential_signing_keypair,sign_api_credential_decision,verify_api_credential_decision,generate_api_credential_recipient_keypair,seal_api_credential_attachment,open_api_credential_attachment,encode_api_credential_recipient_public,load_api_credential_recipient_public,rotate_api_credential_attachment,validate_api_credential_transition

SAMPLE={"credential_id":"credential-045","client_id":"reporting-worker","scopes":["reports:read","jobs:submit"],"created_at":1800000000,"expires_at":1800086400,"status":"pending"}
NEXT={"credential_id":"credential-045","client_id":"reporting-worker","scopes":["reports:read","jobs:submit"],"created_at":1800000000,"expires_at":1800086400,"status":"active"}
INVALID={"credential_id":"credential-045","client_id":"reporting-worker","scopes":[],"created_at":1800000000,"expires_at":1800086400,"status":"pending"}

def test_api_key_broker_business_validation_and_transition():
    record=build_api_credential(SAMPLE); proposed=build_api_credential(NEXT)
    assert validate_api_credential_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["credential_id"]="different-id"
    assert not validate_api_credential_transition(json_bytes(record),json_bytes(build_api_credential(changed)))
    assert not validate_api_credential_transition(json_bytes(record),json_bytes(build_api_credential(dict(SAMPLE))))
    with pytest.raises(ValueError): build_api_credential({})
    with pytest.raises(ValueError): build_api_credential(INVALID)

def test_api_key_broker_signature_tamper_rejection():
    private,public=generate_api_credential_signing_keypair(); record=build_api_credential(SAMPLE); signature=sign_api_credential_decision(record,private)
    assert verify_api_credential_decision(record,signature,public)
    changed=dict(record); changed["credential_id"]+="-changed"
    assert not verify_api_credential_decision(changed,signature,public)

def test_api_key_broker_attachment_context_and_authentication():
    private,public=generate_api_credential_recipient_keypair(); env=seal_api_credential_attachment(b"synthetic evidence",public,"credential-045")
    assert open_api_credential_attachment(env,private,"credential-045")==b"synthetic evidence"
    with pytest.raises(ValueError): open_api_credential_attachment(env,private,"wrong-id")
    other,_=generate_api_credential_recipient_keypair()
    with pytest.raises(ValueError): open_api_credential_attachment(env,other,"credential-045")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_api_credential_attachment(bytes(damaged),private,"credential-045")

def test_api_key_broker_recipient_encoding_and_rotation():
    old,old_public=generate_api_credential_recipient_keypair(); new,new_public=generate_api_credential_recipient_keypair()
    env=seal_api_credential_attachment(b"rotation fixture",old_public,"credential-045")
    rotated=rotate_api_credential_attachment(env,old,new_public,"credential-045")
    assert open_api_credential_attachment(rotated,new,"credential-045")==b"rotation fixture"
    encoded=encode_api_credential_recipient_public(new_public)
    loaded=load_api_credential_recipient_public(encoded)
    assert encode_api_credential_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
