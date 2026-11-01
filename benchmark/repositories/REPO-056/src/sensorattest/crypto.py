"""ECDSA baseline for authenticated sensor readings."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec
def canonical_reading(device_id,sequence,timestamp,metric,value):
 if not device_id or sequence<1 or timestamp<0 or not metric or not isinstance(value,(int,float)):raise ValueError('invalid sensor reading')
 return json.dumps({'device_id':device_id,'sequence':sequence,'timestamp':timestamp,'metric':metric,'value':value},sort_keys=True,separators=(',',':')).encode()
def generate_device_signer():
 p=ec.generate_private_key(ec.SECP256R1());return p,p.public_key()
def sign_reading(record,private):return private.sign(record,ec.ECDSA(hashes.SHA256()))
def verify_reading(record,signature,public):
 try:public.verify(signature,record,ec.ECDSA(hashes.SHA256()));return True
 except (InvalidSignature,ValueError):return False
def export_device_key(public):return public.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_device_key(raw):
 key=serialization.load_der_public_key(raw)
 if not isinstance(key,ec.EllipticCurvePublicKey):raise ValueError('expected EC sensor signing key')
 return key
