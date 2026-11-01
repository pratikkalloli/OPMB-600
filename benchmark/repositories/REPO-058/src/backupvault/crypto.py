"""RSA/X25519 baseline for encrypted versioned backups."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_manifest(backup_id,owner,generation,ciphertext_digest):
 if not backup_id or not owner or generation<1 or len(ciphertext_digest)!=64:raise ValueError('invalid backup manifest')
 return json.dumps({'backup_id':backup_id,'owner':owner,'generation':generation,'ciphertext_sha256':ciphertext_digest},sort_keys=True,separators=(',',':')).encode()
def generate_signer():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_manifest(data,private):return private.sign(data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_manifest(data,sig,public):
 try:public.verify(sig,data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def generate_recipient():
 p=x25519.X25519PrivateKey.generate();return p,p.public_key()
def seal_backup(data,recipient_public):
 e=x25519.X25519PrivateKey.generate();shared=e.exchange(recipient_public);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'backupvault-v1').derive(shared);n=os.urandom(12);return e.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),n,AESGCM(key).encrypt(n,data,b'backupvault-v1')
def open_backup(envelope,private):
 ep,n,ct=envelope;shared=private.exchange(x25519.X25519PublicKey.from_public_bytes(ep));key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'backupvault-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,ct,b'backupvault-v1')
 except InvalidTag as e:raise ValueError('backup authentication failed') from e
def load_recipient(raw):return x25519.X25519PublicKey.from_public_bytes(raw)
def export_signer(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_signer(raw):
 key=serialization.load_pem_public_key(raw)
 if not isinstance(key,rsa.RSAPublicKey):raise ValueError('expected RSA backup signer')
 return key
