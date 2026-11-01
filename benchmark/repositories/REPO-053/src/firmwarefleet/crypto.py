"""RSA baseline for signed synthetic firmware manifests."""
import hashlib,json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa
def canonical_manifest(release_id,family,version,image,minimum_bootloader):
 if not all((release_id,family,version,minimum_bootloader)) or not image: raise ValueError('incomplete firmware release')
 return json.dumps({'release_id':release_id,'family':family,'version':version,'image_sha256':hashlib.sha256(image).hexdigest(),'minimum_bootloader':minimum_bootloader},sort_keys=True,separators=(',',':')).encode()
def generate_release_signer():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_release(manifest,private):return private.sign(manifest,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_release(manifest,signature,public):
 try:public.verify(signature,manifest,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def serialize_signer_public(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_signer_public(raw):
 key=serialization.load_pem_public_key(raw)
 if not isinstance(key,rsa.RSAPublicKey):raise ValueError('expected RSA release key')
 return key
