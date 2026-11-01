"""RSA/X25519 baseline for protected calendar invitations."""
import json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_invitation(invite_id,calendar_id,host,participant,version,start,end,title):
 if not all((invite_id,calendar_id,host,participant,title)) or version<1 or start<0 or end<=start:raise ValueError('invalid invitation')
 return json.dumps({'invite_id':invite_id,'calendar_id':calendar_id,'host':host,'participant':participant,'version':version,'start':start,'end':end,'title':title},sort_keys=True,separators=(',',':')).encode()
def generate_host_signer():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_invitation(data,private):return private.sign(data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_invitation(data,sig,public):
 try:public.verify(sig,data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def generate_participant_keypair():
 p=x25519.X25519PrivateKey.generate();return p,p.public_key()
def protect_event(data,public):
 e=x25519.X25519PrivateKey.generate();shared=e.exchange(public);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'secure-calendar-event-v1').derive(shared);n=os.urandom(12);return e.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),n,AESGCM(key).encrypt(n,data,b'secure-calendar-event-v1')
def open_event(env,private):
 ep,n,ct=env;shared=private.exchange(x25519.X25519PublicKey.from_public_bytes(ep));key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'secure-calendar-event-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,ct,b'secure-calendar-event-v1')
 except InvalidTag as e:raise ValueError('calendar event authentication failed') from e
def export_host_key(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_host_key(raw):
 p=serialization.load_pem_public_key(raw)
 if not isinstance(p,rsa.RSAPublicKey):raise ValueError('expected RSA calendar host key')
 return p
def export_participant_key(public):return public.public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
def load_participant_key(raw):return x25519.X25519PublicKey.from_public_bytes(raw)
