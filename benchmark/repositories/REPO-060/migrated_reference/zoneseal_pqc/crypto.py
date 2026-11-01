"""ML-DSA reference for signed DNS-style zone snapshots."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_zone(zone,serial,records):
 if not zone or serial<1 or not records:raise ValueError('invalid zone snapshot')
 normalized=[]
 for owner,kind,value,ttl in records:
  if not owner or not kind or not value or ttl<1:raise ValueError('invalid resource record')
  normalized.append({'owner':owner.lower().rstrip('.'),'type':kind.upper(),'value':value,'ttl':ttl})
 return json.dumps({'zone':zone.lower().rstrip('.'),'serial':serial,'records':sorted(normalized,key=lambda r:(r['owner'],r['type'],r['value'],r['ttl']))},sort_keys=True,separators=(',',':')).encode()
def generate_zsk():return mldsa.MLDSA65PrivateKey.generate()
def sign_zone(data,private):return private.sign(data,context=b'zoneseal-snapshot-v1')
def verify_zone(data,sig,public):
 try:public.verify(sig,data,context=b'zoneseal-snapshot-v1');return True
 except (InvalidSignature,ValueError):return False
def export_zsk(public):return public.public_bytes_raw()
def load_zsk(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
