"""ML-DSA/ML-KEM notebook reference."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_note(note_id,owner,version,text):
 if not note_id or not owner or version<1 or not text:raise ValueError('invalid note')
 return json.dumps({'note_id':note_id,'owner':owner,'version':version,'text_sha256':hashlib.sha256(text).hexdigest()},sort_keys=True,separators=(',',':')).encode()
def generate_signer():return mldsa.MLDSA65PrivateKey.generate()
def sign_note(record,private):return private.sign(record,context=b'encrypted-notebook-version-v1')
def verify_note(record,sig,public):
 try:public.verify(sig,record,context=b'encrypted-notebook-version-v1');return True
 except (InvalidSignature,ValueError):return False
def generate_owner_keypair():
 p=mlkem.MLKEM768PrivateKey.generate();return p,p.public_key()
def seal_note(text,public):
 shared,ct=public.encapsulate();key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'encrypted-notebook-v1').derive(shared);n=os.urandom(12);return ct,n,AESGCM(key).encrypt(n,text,b'encrypted-notebook-v1')
def open_note(env,private):
 ct,n,cipher=env;shared=private.decapsulate(ct);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'encrypted-notebook-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,cipher,b'encrypted-notebook-v1')
 except InvalidTag as e:raise ValueError('note authentication failed') from e
def export_signer(public):return public.public_bytes_raw()
def load_signer(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
def export_owner(public):return public.public_bytes_raw()
def load_owner(raw):return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
