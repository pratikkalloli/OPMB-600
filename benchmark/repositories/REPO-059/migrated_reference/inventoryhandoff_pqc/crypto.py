"""ML-DSA reference for signed inventory custody transfers."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_transfer(item_id,batch_id,sequence,timestamp,sender,recipient):
 if not all((item_id,batch_id,sender,recipient)) or sender==recipient or sequence<1 or timestamp<0:raise ValueError('invalid inventory transfer')
 return json.dumps({'item_id':item_id,'batch_id':batch_id,'sequence':sequence,'timestamp':timestamp,'sender':sender,'recipient':recipient},sort_keys=True,separators=(',',':')).encode()
def generate_actor():return mldsa.MLDSA65PrivateKey.generate()
def sign_transfer(record,private):return private.sign(record,context=b'inventory-handoff-v1')
def verify_transfer(record,sig,public):
 try:public.verify(sig,record,context=b'inventory-handoff-v1');return True
 except (InvalidSignature,ValueError):return False
def export_actor(public):return public.public_bytes_raw()
def load_actor(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
