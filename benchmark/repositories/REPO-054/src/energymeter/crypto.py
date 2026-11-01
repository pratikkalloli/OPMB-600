"""ECDSA baseline for simulated energy meter readings."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec
def canonical_reading(meter_id,sequence,timestamp,value,unit):
 if not meter_id or sequence<1 or timestamp<0 or value<0 or not unit:raise ValueError('invalid meter reading')
 return json.dumps({'meter_id':meter_id,'sequence':sequence,'timestamp':timestamp,'value':float(value),'unit':unit},sort_keys=True,separators=(',',':')).encode()
def generate_meter_keypair():
 p=ec.generate_private_key(ec.SECP256R1());return p,p.public_key()
def sign_reading(record,private):return private.sign(record,ec.ECDSA(hashes.SHA256()))
def verify_reading(record,sig,public):
 try:public.verify(sig,record,ec.ECDSA(hashes.SHA256()));return True
 except (InvalidSignature,ValueError):return False
def export_meter_key(public):return public.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_meter_key(raw):
 p=serialization.load_der_public_key(raw)
 if not isinstance(p,ec.EllipticCurvePublicKey):raise ValueError('expected EC meter key')
 return p
