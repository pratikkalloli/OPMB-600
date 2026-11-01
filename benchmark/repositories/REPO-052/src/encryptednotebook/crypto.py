"""Classical RSA/X25519 notebook protection baseline."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_note(note_id,owner,version,text):
 if not note_id or not owner or version<1 or not text:raise ValueError('invalid note')
 return json.dumps({'note_id':note_id,'owner':owner,'version':version,'text_sha256':hashlib.sha256(text).hexdigest()},sort_keys=True,separators=(',',':')).encode()
def generate_signer():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_note(record,private):return private.sign(record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_note(record,sig,public):
 try:public.verify(sig,record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def generate_owner_keypair():
 p=x25519.X25519PrivateKey.generate();return p,p.public_key()
def seal_note(text,public):
 e=x25519.X25519PrivateKey.generate();shared=e.exchange(public);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'encrypted-notebook-v1').derive(shared);n=os.urandom(12);return e.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),n,AESGCM(key).encrypt(n,text,b'encrypted-notebook-v1')
def open_note(env,private):
 ep,n,ct=env;shared=private.exchange(x25519.X25519PublicKey.from_public_bytes(ep));key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'encrypted-notebook-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,ct,b'encrypted-notebook-v1')
 except InvalidTag as e:raise ValueError('note authentication failed') from e
def export_signer(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_signer(raw):
 p=serialization.load_pem_public_key(raw)
 if not isinstance(p,rsa.RSAPublicKey):raise ValueError('expected RSA notebook signer')
 return p

def export_owner(public):return public.public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
def load_owner(raw):return x25519.X25519PublicKey.from_public_bytes(raw)
