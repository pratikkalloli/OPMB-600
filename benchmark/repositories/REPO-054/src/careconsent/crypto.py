"""RSA-PSS baseline for research consent authorization records."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa
def canonical_consent(consent_id,subject,study,scope,expires_at,revision):
 if not all((consent_id,subject,study,scope)) or expires_at<=0 or revision<1:raise ValueError('invalid consent record')
 return json.dumps({'consent_id':consent_id,'subject':subject,'study':study,'scope':scope,'expires_at':expires_at,'revision':revision},sort_keys=True,separators=(',',':')).encode()
def generate_authority():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_consent(record,private):return private.sign(record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_consent(record,signature,public):
 try:public.verify(signature,record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def export_authority(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_authority(raw):
 key=serialization.load_pem_public_key(raw)
 if not isinstance(key,rsa.RSAPublicKey):raise ValueError('expected RSA consent authority')
 return key
