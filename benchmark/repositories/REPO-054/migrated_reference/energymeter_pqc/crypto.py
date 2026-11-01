"""ML-DSA reference for simulated energy meter readings."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_reading(meter_id,sequence,timestamp,value,unit):
 if not meter_id or sequence<1 or timestamp<0 or value<0 or not unit:raise ValueError('invalid meter reading')
 return json.dumps({'meter_id':meter_id,'sequence':sequence,'timestamp':timestamp,'value':float(value),'unit':unit},sort_keys=True,separators=(',',':')).encode()
def generate_meter_keypair():return mldsa.MLDSA65PrivateKey.generate()
def sign_reading(record,private):return private.sign(record,context=b'energymeter-reading-v1')
def verify_reading(record,sig,public):
 try:public.verify(sig,record,context=b'energymeter-reading-v1');return True
 except (InvalidSignature,ValueError):return False
def export_meter_key(public):return public.public_bytes_raw()
def load_meter_key(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
