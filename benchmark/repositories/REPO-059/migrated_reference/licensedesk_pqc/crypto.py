"""ML-DSA reference for signed synthetic software licenses."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_license(license_id,product,installation,features,issued_at,expires_at):
 if not all((license_id,product,installation,features)) or issued_at<0 or expires_at<=issued_at:raise ValueError('invalid license')
 return json.dumps({'license_id':license_id,'product':product,'installation':installation,'features':sorted(set(features)),'issued_at':issued_at,'expires_at':expires_at},sort_keys=True,separators=(',',':')).encode()
def generate_authority():return mldsa.MLDSA65PrivateKey.generate()
def sign_license(record,private):return private.sign(record,context=b'licensedesk-grant-v1')
def verify_license(record,sig,public):
 try:public.verify(sig,record,context=b'licensedesk-grant-v1');return True
 except (InvalidSignature,ValueError):return False
def export_authority(public):return public.public_bytes_raw()
def load_authority(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
