import pytest
from energymeter_pqc.crypto import generate_meter_keypair,canonical_reading
from energymeter_pqc.service import EnergyMeter
def signed(sk,mid,seq,ts,val):return sk.sign(canonical_reading(mid,seq,ts,val,'kWh'),context=b'energymeter-reading-v1')
def test_register_readings_audit_and_rotation(tmp_path):
 sk=generate_meter_keypair();m=EnergyMeter(tmp_path/'e.db');m.register_meter('m1',sk.public_key());assert m.submit_reading('m1',1,10,3.5,'kWh',signed(sk,'m1',1,10,3.5));sk2=generate_meter_keypair();assert m.rotate_meter_key('m1',sk2.public_key())==2;assert m.submit_reading('m1',2,11,4,'kWh',signed(sk2,'m1',2,11,4));assert m.verify_history('m1');assert [r[-1] for r in m.audit_history('m1')]==[1,2]
def test_replay_tamper_time_and_bad_values(tmp_path):
 sk=generate_meter_keypair();m=EnergyMeter(tmp_path/'e.db');m.register_meter('m',sk.public_key())
 with pytest.raises(PermissionError):m.submit_reading('m',1,2,1,'kWh',b'bad')
 with pytest.raises(ValueError):canonical_reading('m',0,1,1,'kWh')
