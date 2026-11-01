"""Classical sender signatures and recipient encryption for synthetic mail."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_message(message_id,sender,recipient,created_at,body):
 if not all((message_id,sender,recipient,body)) or sender==recipient or created_at<0:raise ValueError('invalid message')
 return json.dumps({'id':message_id,'sender':sender,'recipient':recipient,'created_at':created_at,'body_sha256':hashlib.sha256(body).hexdigest()},sort_keys=True,separators=(',',':')).encode()
def generate_sender():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_message(data,private):return private.sign(data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_message(data,sig,public):
 try:public.verify(sig,data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def generate_recipient():
 p=x25519.X25519PrivateKey.generate();return p,p.public_key()
def seal_message(body,recipient_public):
 eph=x25519.X25519PrivateKey.generate();shared=eph.exchange(recipient_public);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'securemailbox-v1').derive(shared);nonce=os.urandom(12);return eph.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),nonce,AESGCM(key).encrypt(nonce,body,b'securemailbox-v1')
def open_message(envelope,recipient_private):
 ep,nonce,ct=envelope;shared=recipient_private.exchange(x25519.X25519PublicKey.from_public_bytes(ep));key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'securemailbox-v1').derive(shared)
 try:return AESGCM(key).decrypt(nonce,ct,b'securemailbox-v1')
 except InvalidTag as e:raise ValueError('message authentication failed') from e
def load_recipient(raw):return x25519.X25519PublicKey.from_public_bytes(raw)
def export_sender(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_sender(raw):
 key=serialization.load_pem_public_key(raw)
 if not isinstance(key,rsa.RSAPublicKey):raise ValueError('expected RSA sender key')
 return key
