"""ML-DSA/ML-KEM data marketplace reference."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_manifest(asset_id,provider,version,metadata,data):
 if not all((asset_id,provider,metadata,data)) or version<1:raise ValueError('invalid asset manifest')
 return json.dumps({'asset_id':asset_id,'provider':provider,'version':version,'metadata_sha256':hashlib.sha256(metadata).hexdigest(),'data_sha256':hashlib.sha256(data).hexdigest()},sort_keys=True,separators=(',',':')).encode()
def generate_provider_signer():return mldsa.MLDSA65PrivateKey.generate()
def sign_manifest(data,private):return private.sign(data,context=b'datamarketplace-manifest-v1')
def verify_manifest(data,sig,public):
 try:public.verify(sig,data,context=b'datamarketplace-manifest-v1');return True
 except (InvalidSignature,ValueError):return False
def generate_consumer_keypair():
 p=mlkem.MLKEM768PrivateKey.generate();return p,p.public_key()
def seal_asset(data,public):
 shared,ct=public.encapsulate();key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'datamarketplace-v1').derive(shared);n=os.urandom(12);return ct,n,AESGCM(key).encrypt(n,data,b'datamarketplace-v1')
def open_asset(env,private):
 ct,n,cipher=env;shared=private.decapsulate(ct);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'datamarketplace-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,cipher,b'datamarketplace-v1')
 except InvalidTag as e:raise ValueError('asset authentication failed') from e
def export_provider(public):return public.public_bytes_raw()
def load_provider(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
def export_consumer(public):return public.public_bytes_raw()
def load_consumer(raw):return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
