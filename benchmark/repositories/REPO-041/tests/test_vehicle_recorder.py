import json,pytest
from vehicle_recorder.service import build_vehicle_event,generate_vehicle_event_signing_keypair,sign_vehicle_event_decision,verify_vehicle_event_decision,generate_vehicle_event_recipient_keypair,seal_vehicle_event_attachment,open_vehicle_event_attachment,encode_vehicle_event_recipient_public,load_vehicle_event_recipient_public,rotate_vehicle_event_attachment,validate_vehicle_event_transition

SAMPLE={"event_id":"event-041","vehicle_id":"vehicle-5","trip_id":"trip-22","sequence":1,"event_time":1800000000,"sensor_digest":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","integrity_state":"captured"}
NEXT={"event_id":"event-041","vehicle_id":"vehicle-5","trip_id":"trip-22","sequence":1,"event_time":1800000000,"sensor_digest":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","integrity_state":"sealed"}
INVALID={"event_id":"event-041","vehicle_id":"vehicle-5","trip_id":"trip-22","sequence":-1,"event_time":1800000000,"sensor_digest":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","integrity_state":"captured"}

def test_vehicle_recorder_business_validation_and_transition():
    record=build_vehicle_event(SAMPLE); proposed=build_vehicle_event(NEXT)
    assert validate_vehicle_event_transition(json_bytes(record),json_bytes(proposed))
    changed=dict(NEXT); changed["event_id"]="different-id"
    assert not validate_vehicle_event_transition(json_bytes(record),json_bytes(build_vehicle_event(changed)))
    assert not validate_vehicle_event_transition(json_bytes(record),json_bytes(build_vehicle_event(dict(SAMPLE))))
    with pytest.raises(ValueError): build_vehicle_event({})
    with pytest.raises(ValueError): build_vehicle_event(INVALID)

def test_vehicle_recorder_signature_tamper_rejection():
    private,public=generate_vehicle_event_signing_keypair(); record=build_vehicle_event(SAMPLE); signature=sign_vehicle_event_decision(record,private)
    assert verify_vehicle_event_decision(record,signature,public)
    changed=dict(record); changed["event_id"]+="-changed"
    assert not verify_vehicle_event_decision(changed,signature,public)

def test_vehicle_recorder_attachment_context_and_authentication():
    private,public=generate_vehicle_event_recipient_keypair(); env=seal_vehicle_event_attachment(b"synthetic evidence",public,"event-041")
    assert open_vehicle_event_attachment(env,private,"event-041")==b"synthetic evidence"
    with pytest.raises(ValueError): open_vehicle_event_attachment(env,private,"wrong-id")
    other,_=generate_vehicle_event_recipient_keypair()
    with pytest.raises(ValueError): open_vehicle_event_attachment(env,other,"event-041")
    damaged=bytearray(env); damaged[-1]^=1
    with pytest.raises(ValueError): open_vehicle_event_attachment(bytes(damaged),private,"event-041")

def test_vehicle_recorder_recipient_encoding_and_rotation():
    old,old_public=generate_vehicle_event_recipient_keypair(); new,new_public=generate_vehicle_event_recipient_keypair()
    env=seal_vehicle_event_attachment(b"rotation fixture",old_public,"event-041")
    rotated=rotate_vehicle_event_attachment(env,old,new_public,"event-041")
    assert open_vehicle_event_attachment(rotated,new,"event-041")==b"rotation fixture"
    encoded=encode_vehicle_event_recipient_public(new_public)
    loaded=load_vehicle_event_recipient_public(encoded)
    assert encode_vehicle_event_recipient_public(loaded)==encoded

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
