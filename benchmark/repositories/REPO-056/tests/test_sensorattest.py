import pytest
from sensorattest.crypto import generate_device_signer,canonical_reading,export_device_key,load_device_key
from sensorattest.service import SensorAttest
def test_signed_sequence_and_replay_rejection(tmp_path):
 sk,pk=generate_device_signer();app=SensorAttest(tmp_path/'s.db');app.enroll('s1',pk);r=canonical_reading('s1',1,50,'temperature',22.5);assert app.submit('s1',1,50,'temperature',22.5,sk.sign(r,__import__('cryptography').hazmat.primitives.asymmetric.ec.ECDSA(__import__('cryptography').hazmat.primitives.hashes.SHA256())));assert app.last_sequence('s1')==1
 with pytest.raises(ValueError):app.submit('s1',1,50,'temperature',22.5,b'bad')
def test_wrong_signature_and_inactive_sensor_rejected(tmp_path):
 sk,pk=generate_device_signer();other,_=generate_device_signer();app=SensorAttest(tmp_path/'s.db');app.enroll('s',pk);record=canonical_reading('s',1,3,'humidity',40)
 with pytest.raises(PermissionError):app.submit('s',1,3,'humidity',40,other.sign(record,__import__('cryptography').hazmat.primitives.asymmetric.ec.ECDSA(__import__('cryptography').hazmat.primitives.hashes.SHA256())))
 assert app.deactivate('s')
 with pytest.raises(PermissionError):app.submit('s',1,3,'humidity',40,sk.sign(record,__import__('cryptography').hazmat.primitives.asymmetric.ec.ECDSA(__import__('cryptography').hazmat.primitives.hashes.SHA256())))
def test_key_serialization():
 _,pk=generate_device_signer();assert load_device_key(export_device_key(pk)) is not None
