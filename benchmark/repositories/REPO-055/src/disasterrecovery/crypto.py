"""RSA/X25519 baseline for encrypted versioned backups."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_recovery_manifest(snapshot_id,system_id,created_at,ciphertext_digest):
 if not snapshot_id or not system_id or created_at<1 or len(ciphertext_digest)!=64:raise ValueError('invalid recovery manifest')
 return json.dumps({'snapshot_id':snapshot_id,'system_id':system_id,'created_at':created_at,'ciphertext_sha256':ciphertext_digest},sort_keys=True,separators=(',',':')).encode()
def generate_recovery_signer():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_recovery_manifest(data,private):return private.sign(data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_recovery_manifest(data,sig,public):
 try:public.verify(sig,data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def generate_recovery_keypair():
 p=x25519.X25519PrivateKey.generate();return p,p.public_key()
def seal_snapshot(data,recipient_public):
 e=x25519.X25519PrivateKey.generate();shared=e.exchange(recipient_public);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'disaster-recovery-snapshot-v1').derive(shared);n=os.urandom(12);return e.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),n,AESGCM(key).encrypt(n,data,b'disaster-recovery-snapshot-v1')
def open_snapshot(envelope,private):
 ep,n,ct=envelope;shared=private.exchange(x25519.X25519PublicKey.from_public_bytes(ep));key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'disaster-recovery-snapshot-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,ct,b'disaster-recovery-snapshot-v1')
 except InvalidTag as e:raise ValueError('snapshot authentication failed') from e
def load_recovery_recipient(raw):return x25519.X25519PublicKey.from_public_bytes(raw)
def export_recovery_signer(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_recovery_signer(raw):
 key=serialization.load_pem_public_key(raw)
 if not isinstance(key,rsa.RSAPublicKey):raise ValueError('expected RSA backup signer')
 return key

def export_recovery_recipient(public):return public.public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
