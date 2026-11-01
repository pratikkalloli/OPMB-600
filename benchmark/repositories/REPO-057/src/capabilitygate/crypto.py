"""RSA-PSS baseline for short-lived API capabilities."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa
def canonical_capability(token_id,principal,resource,action,expires_at):
 if not all((token_id,principal,resource,action)) or expires_at<=0:raise ValueError('invalid capability')
 return json.dumps({'jti':token_id,'sub':principal,'resource':resource,'action':action,'exp':expires_at},sort_keys=True,separators=(',',':')).encode()
def generate_issuer():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_capability(payload,private):return private.sign(payload,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_capability(payload,sig,public):
 try:public.verify(sig,payload,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def export_issuer(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_issuer(raw):
 key=serialization.load_pem_public_key(raw)
 if not isinstance(key,rsa.RSAPublicKey):raise ValueError('expected RSA issuer key')
 return key
