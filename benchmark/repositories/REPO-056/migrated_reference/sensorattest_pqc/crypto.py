"""ML-DSA reference for authenticated sensor readings."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_reading(device_id,sequence,timestamp,metric,value):
 if not device_id or sequence<1 or timestamp<0 or not metric or not isinstance(value,(int,float)):raise ValueError('invalid sensor reading')
 return json.dumps({'device_id':device_id,'sequence':sequence,'timestamp':timestamp,'metric':metric,'value':value},sort_keys=True,separators=(',',':')).encode()
def generate_device_signer():return mldsa.MLDSA65PrivateKey.generate()
def sign_reading(record,private):return private.sign(record,context=b'sensorattest-reading-v1')
def verify_reading(record,signature,public):
 try:public.verify(signature,record,context=b'sensorattest-reading-v1');return True
 except (InvalidSignature,ValueError):return False
def export_device_key(public):return public.public_bytes_raw()
def load_device_key(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
