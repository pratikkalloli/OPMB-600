"""ML-DSA/ML-KEM message authenticity and recipient encryption."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_message(message_id,sender,recipient,created_at,body):
 if not all((message_id,sender,recipient,body)) or sender==recipient or created_at<0:raise ValueError('invalid message')
 return json.dumps({'id':message_id,'sender':sender,'recipient':recipient,'created_at':created_at,'body_sha256':hashlib.sha256(body).hexdigest()},sort_keys=True,separators=(',',':')).encode()
def generate_sender():return mldsa.MLDSA65PrivateKey.generate()
def sign_message(data,private):return private.sign(data,context=b'securemailbox-message-v1')
def verify_message(data,sig,public):
 try:public.verify(sig,data,context=b'securemailbox-message-v1');return True
 except (InvalidSignature,ValueError):return False
def generate_recipient():
 p=mlkem.MLKEM768PrivateKey.generate();return p,p.public_key()
def seal_message(body,recipient_public):
 shared,ct=recipient_public.encapsulate();key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'securemailbox-v1').derive(shared);nonce=os.urandom(12);return ct,nonce,AESGCM(key).encrypt(nonce,body,b'securemailbox-v1')
def open_message(envelope,recipient_private):
 ct,nonce,ciphertext=envelope;shared=recipient_private.decapsulate(ct);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'securemailbox-v1').derive(shared)
 try:return AESGCM(key).decrypt(nonce,ciphertext,b'securemailbox-v1')
 except InvalidTag as e:raise ValueError('message authentication failed') from e
def load_recipient(raw):return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
def export_sender(public):return public.public_bytes_raw()
def load_sender(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
