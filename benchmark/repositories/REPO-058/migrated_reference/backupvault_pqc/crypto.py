"""ML-DSA/ML-KEM reference for encrypted versioned backups."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_manifest(backup_id,owner,generation,ciphertext_digest):
 if not backup_id or not owner or generation<1 or len(ciphertext_digest)!=64:raise ValueError('invalid backup manifest')
 return json.dumps({'backup_id':backup_id,'owner':owner,'generation':generation,'ciphertext_sha256':ciphertext_digest},sort_keys=True,separators=(',',':')).encode()
def generate_signer():return mldsa.MLDSA65PrivateKey.generate()
def sign_manifest(data,private):return private.sign(data,context=b'backupvault-manifest-v1')
def verify_manifest(data,sig,public):
 try:public.verify(sig,data,context=b'backupvault-manifest-v1');return True
 except (InvalidSignature,ValueError):return False
def generate_recipient():
 p=mlkem.MLKEM768PrivateKey.generate();return p,p.public_key()
def seal_backup(data,recipient_public):
 shared,ct=recipient_public.encapsulate();key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'backupvault-v1').derive(shared);n=os.urandom(12);return ct,n,AESGCM(key).encrypt(n,data,b'backupvault-v1')
def open_backup(envelope,private):
 ct,n,cipher= envelope;shared=private.decapsulate(ct);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'backupvault-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,cipher,b'backupvault-v1')
 except InvalidTag as e:raise ValueError('backup authentication failed') from e
def load_recipient(raw):return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
def export_signer(public):return public.public_bytes_raw()
def load_signer(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
