"""RSA/X25519 baseline for signed and protected data assets."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_manifest(asset_id,provider,version,metadata,data):
 if not all((asset_id,provider,metadata,data)) or version<1:raise ValueError('invalid asset manifest')
 return json.dumps({'asset_id':asset_id,'provider':provider,'version':version,'metadata_sha256':hashlib.sha256(metadata).hexdigest(),'data_sha256':hashlib.sha256(data).hexdigest()},sort_keys=True,separators=(',',':')).encode()
def generate_provider_signer():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_manifest(data,private):return private.sign(data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_manifest(data,sig,public):
 try:public.verify(sig,data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def generate_consumer_keypair():
 p=x25519.X25519PrivateKey.generate();return p,p.public_key()
def seal_asset(data,public):
 e=x25519.X25519PrivateKey.generate();shared=e.exchange(public);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'datamarketplace-v1').derive(shared);n=os.urandom(12);return e.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),n,AESGCM(key).encrypt(n,data,b'datamarketplace-v1')
def open_asset(env,private):
 ep,n,ct=env;shared=private.exchange(x25519.X25519PublicKey.from_public_bytes(ep));key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'datamarketplace-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,ct,b'datamarketplace-v1')
 except InvalidTag as e:raise ValueError('asset authentication failed') from e
def export_provider(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_provider(raw):
 key=serialization.load_pem_public_key(raw)
 if not isinstance(key,rsa.RSAPublicKey):raise ValueError('expected RSA provider key')
 return key
def export_consumer(public):return public.public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
def load_consumer(raw):return x25519.X25519PublicKey.from_public_bytes(raw)
