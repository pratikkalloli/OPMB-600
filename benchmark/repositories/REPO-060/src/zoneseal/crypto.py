"""ECDSA baseline for signed DNS-style zone snapshots."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec
def canonical_zone(zone,serial,records):
 if not zone or serial<1 or not records:raise ValueError('invalid zone snapshot')
 normalized=[]
 for owner,kind,value,ttl in records:
  if not owner or not kind or not value or ttl<1:raise ValueError('invalid resource record')
  normalized.append({'owner':owner.lower().rstrip('.'),'type':kind.upper(),'value':value,'ttl':ttl})
 return json.dumps({'zone':zone.lower().rstrip('.'),'serial':serial,'records':sorted(normalized,key=lambda r:(r['owner'],r['type'],r['value'],r['ttl']))},sort_keys=True,separators=(',',':')).encode()
def generate_zsk():
 p=ec.generate_private_key(ec.SECP256R1());return p,p.public_key()
def sign_zone(data,private):return private.sign(data,ec.ECDSA(hashes.SHA256()))
def verify_zone(data,sig,public):
 try:public.verify(sig,data,ec.ECDSA(hashes.SHA256()));return True
 except (InvalidSignature,ValueError):return False
def export_zsk(public):return public.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_zsk(raw):
 key=serialization.load_der_public_key(raw)
 if not isinstance(key,ec.EllipticCurvePublicKey):raise ValueError('expected EC zone signing key')
 return key
