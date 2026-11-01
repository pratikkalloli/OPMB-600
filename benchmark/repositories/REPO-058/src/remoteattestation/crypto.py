"""RSA/X25519 baseline for simulated signed workload evidence."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_evidence(evidence_id,workload,measurement,policy,issued_at,expires_at):
 if not all((evidence_id,workload,measurement,policy)) or issued_at<0 or expires_at<=issued_at:raise ValueError('invalid evidence package')
 return json.dumps({'evidence_id':evidence_id,'workload':workload,'measurement':measurement,'policy':policy,'issued_at':issued_at,'expires_at':expires_at},sort_keys=True,separators=(',',':')).encode()
def generate_attestor():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_evidence(record,private):return private.sign(record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_evidence_signature(record,sig,public):
 try:public.verify(sig,record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def generate_verifier_keypair():
 p=x25519.X25519PrivateKey.generate();return p,p.public_key()
def protect_evidence(record,public):
 e=x25519.X25519PrivateKey.generate();shared=e.exchange(public);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'remote-attestation-evidence-v1').derive(shared);n=os.urandom(12);return e.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),n,AESGCM(key).encrypt(n,record,b'remote-attestation-evidence-v1')
def open_evidence(env,private):
 ep,n,ct=env;shared=private.exchange(x25519.X25519PublicKey.from_public_bytes(ep));key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'remote-attestation-evidence-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,ct,b'remote-attestation-evidence-v1')
 except InvalidTag as e:raise ValueError('evidence authentication failed') from e
def export_attestor(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_attestor(raw):
 p=serialization.load_pem_public_key(raw)
 if not isinstance(p,rsa.RSAPublicKey):raise ValueError('expected RSA attestor key')
 return p
