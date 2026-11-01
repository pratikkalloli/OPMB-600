"""RSA-PSS baseline for signed synthetic software licenses."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa
def canonical_license(license_id,product,installation,features,issued_at,expires_at):
 if not all((license_id,product,installation,features)) or issued_at<0 or expires_at<=issued_at:raise ValueError('invalid license')
 return json.dumps({'license_id':license_id,'product':product,'installation':installation,'features':sorted(set(features)),'issued_at':issued_at,'expires_at':expires_at},sort_keys=True,separators=(',',':')).encode()
def generate_authority():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_license(record,private):return private.sign(record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_license(record,sig,public):
 try:public.verify(sig,record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def export_authority(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_authority(raw):
 key=serialization.load_pem_public_key(raw)
 if not isinstance(key,rsa.RSAPublicKey):raise ValueError('expected RSA license authority')
 return key
