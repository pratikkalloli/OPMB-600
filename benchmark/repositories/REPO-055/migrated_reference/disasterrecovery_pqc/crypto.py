"""ML-DSA/ML-KEM reference for encrypted versioned backups."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_recovery_manifest(snapshot_id,system_id,created_at,ciphertext_digest):
 if not snapshot_id or not system_id or created_at<1 or len(ciphertext_digest)!=64:raise ValueError('invalid recovery manifest')
 return json.dumps({'snapshot_id':snapshot_id,'system_id':system_id,'created_at':created_at,'ciphertext_sha256':ciphertext_digest},sort_keys=True,separators=(',',':')).encode()
def generate_recovery_signer():return mldsa.MLDSA65PrivateKey.generate()
def sign_recovery_manifest(data,private):return private.sign(data,context=b'disasterrecovery-manifest-v1')
def verify_recovery_manifest(data,sig,public):
 try:public.verify(sig,data,context=b'disasterrecovery-manifest-v1');return True
 except (InvalidSignature,ValueError):return False
def generate_recovery_keypair():
 p=mlkem.MLKEM768PrivateKey.generate();return p,p.public_key()
def seal_snapshot(data,recipient_public):
 shared,ct=recipient_public.encapsulate();key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'disaster-recovery-snapshot-v1').derive(shared);n=os.urandom(12);return ct,n,AESGCM(key).encrypt(n,data,b'disaster-recovery-snapshot-v1')
def open_snapshot(envelope,private):
 ct,n,cipher= envelope;shared=private.decapsulate(ct);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'disaster-recovery-snapshot-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,cipher,b'disaster-recovery-snapshot-v1')
 except InvalidTag as e:raise ValueError('snapshot authentication failed') from e
def load_recovery_recipient(raw):return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
def export_recovery_signer(public):return public.public_bytes_raw()
def load_recovery_signer(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)

def export_recovery_recipient(public):return public.public_bytes_raw()
