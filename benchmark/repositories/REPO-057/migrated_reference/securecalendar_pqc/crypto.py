"""ML-DSA/ML-KEM protected calendar invitation reference."""
import json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_invitation(invite_id,calendar_id,host,participant,version,start,end,title):
 if not all((invite_id,calendar_id,host,participant,title)) or version<1 or start<0 or end<=start:raise ValueError('invalid invitation')
 return json.dumps({'invite_id':invite_id,'calendar_id':calendar_id,'host':host,'participant':participant,'version':version,'start':start,'end':end,'title':title},sort_keys=True,separators=(',',':')).encode()
def generate_host_signer():return mldsa.MLDSA65PrivateKey.generate()
def sign_invitation(data,private):return private.sign(data,context=b'secure-calendar-invitation-v1')
def verify_invitation(data,sig,public):
 try:public.verify(sig,data,context=b'secure-calendar-invitation-v1');return True
 except (InvalidSignature,ValueError):return False
def generate_participant_keypair():
 p=mlkem.MLKEM768PrivateKey.generate();return p,p.public_key()
def protect_event(data,public):
 shared,ct=public.encapsulate();key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'secure-calendar-event-v1').derive(shared);n=os.urandom(12);return ct,n,AESGCM(key).encrypt(n,data,b'secure-calendar-event-v1')
def open_event(env,private):
 ct,n,cipher=env;shared=private.decapsulate(ct);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'secure-calendar-event-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,cipher,b'secure-calendar-event-v1')
 except InvalidTag as e:raise ValueError('calendar event authentication failed') from e
def export_host_key(public):return public.public_bytes_raw()
def load_host_key(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
def export_participant_key(public):return public.public_bytes_raw()
def load_participant_key(raw):return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
