import pytest
from energymeter.crypto import generate_meter_keypair,canonical_reading
from energymeter.service import EnergyMeter
def signed(sk,mid,seq,ts,val):
 rec=canonical_reading(mid,seq,ts,val,'kWh')
 try:from cryptography.hazmat.primitives.asymmetric import ec;from cryptography.hazmat.primitives import hashes;return sk.sign(rec,ec.ECDSA(hashes.SHA256()))
 except TypeError:return sk.sign(rec,context=b'energymeter-reading-v1')
def test_register_readings_audit_and_rotation(tmp_path):
 sk,pk=generate_meter_keypair();m=EnergyMeter(tmp_path/'e.db');m.register_meter('m1',pk);assert m.submit_reading('m1',1,10,3.5,'kWh',signed(sk,'m1',1,10,3.5));sk2,pk2=generate_meter_keypair();assert m.rotate_meter_key('m1',pk2)==2;assert m.submit_reading('m1',2,11,4,'kWh',signed(sk2,'m1',2,11,4));assert m.verify_history('m1');assert [r[-1] for r in m.audit_history('m1')]==[1,2]
def test_replay_tamper_time_and_bad_values(tmp_path):
 sk,pk=generate_meter_keypair();m=EnergyMeter(tmp_path/'e.db');m.register_meter('m',pk)
 with pytest.raises(PermissionError):m.submit_reading('m',1,2,1,'kWh',b'bad')
 with pytest.raises(ValueError):canonical_reading('m',0,1,1,'kWh')
