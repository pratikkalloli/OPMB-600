"""ECDSA baseline for signed inventory custody transfers."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec
def canonical_transfer(item_id,batch_id,sequence,timestamp,sender,recipient):
 if not all((item_id,batch_id,sender,recipient)) or sender==recipient or sequence<1 or timestamp<0:raise ValueError('invalid inventory transfer')
 return json.dumps({'item_id':item_id,'batch_id':batch_id,'sequence':sequence,'timestamp':timestamp,'sender':sender,'recipient':recipient},sort_keys=True,separators=(',',':')).encode()
def generate_actor():
 p=ec.generate_private_key(ec.SECP256R1());return p,p.public_key()
def sign_transfer(record,private):return private.sign(record,ec.ECDSA(hashes.SHA256()))
def verify_transfer(record,sig,public):
 try:public.verify(sig,record,ec.ECDSA(hashes.SHA256()));return True
 except (InvalidSignature,ValueError):return False
def export_actor(public):return public.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_actor(raw):
 p=serialization.load_der_public_key(raw)
 if not isinstance(p,ec.EllipticCurvePublicKey):raise ValueError('expected EC inventory actor key')
 return p
