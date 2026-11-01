"""ML-DSA/ML-KEM simulation reference for workload evidence."""
import json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_evidence(evidence_id,workload,measurement,policy,issued_at,expires_at):
 if not all((evidence_id,workload,measurement,policy)) or issued_at<0 or expires_at<=issued_at:raise ValueError('invalid evidence package')
 return json.dumps({'evidence_id':evidence_id,'workload':workload,'measurement':measurement,'policy':policy,'issued_at':issued_at,'expires_at':expires_at},sort_keys=True,separators=(',',':')).encode()
def generate_attestor():return mldsa.MLDSA65PrivateKey.generate()
def sign_evidence(record,private):return private.sign(record,context=b'remote-attestation-evidence-v1')
def verify_evidence_signature(record,sig,public):
 try:public.verify(sig,record,context=b'remote-attestation-evidence-v1');return True
 except (InvalidSignature,ValueError):return False
def generate_verifier_keypair():
 p=mlkem.MLKEM768PrivateKey.generate();return p,p.public_key()
def protect_evidence(record,public):
 shared,ct=public.encapsulate();key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'remote-attestation-evidence-v1').derive(shared);n=os.urandom(12);return ct,n,AESGCM(key).encrypt(n,record,b'remote-attestation-evidence-v1')
def open_evidence(env,private):
 ct,n,cipher=env;shared=private.decapsulate(ct);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'remote-attestation-evidence-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,cipher,b'remote-attestation-evidence-v1')
 except InvalidTag as e:raise ValueError('evidence authentication failed') from e
def export_attestor(public):return public.public_bytes_raw()
def load_attestor(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
