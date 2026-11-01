"""ML-DSA reference for signed synthetic firmware manifests."""
import hashlib,json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_manifest(release_id,family,version,image,minimum_bootloader):
 if not all((release_id,family,version,minimum_bootloader)) or not image:raise ValueError('incomplete firmware release')
 return json.dumps({'release_id':release_id,'family':family,'version':version,'image_sha256':hashlib.sha256(image).hexdigest(),'minimum_bootloader':minimum_bootloader},sort_keys=True,separators=(',',':')).encode()
def generate_release_signer():return mldsa.MLDSA65PrivateKey.generate()
def sign_release(manifest,private):return private.sign(manifest,context=b'firmwarefleet-release-v1')
def verify_release(manifest,signature,public):
 try:public.verify(signature,manifest,context=b'firmwarefleet-release-v1');return True
 except (InvalidSignature,ValueError):return False
def serialize_signer_public(public):return public.public_bytes_raw()
def load_signer_public(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
