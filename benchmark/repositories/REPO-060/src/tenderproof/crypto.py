"""RSA/X25519 baseline for signed confidential procurement bids."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_bid(tender_id,bidder,bid_id,amount_minor,proposal,submitted_at):
 if not all((tender_id,bidder,bid_id,proposal)) or amount_minor<1 or submitted_at<0:raise ValueError('invalid bid')
 return json.dumps({'tender_id':tender_id,'bidder':bidder,'bid_id':bid_id,'amount_minor':amount_minor,'proposal_sha256':hashlib.sha256(proposal).hexdigest(),'submitted_at':submitted_at},sort_keys=True,separators=(',',':')).encode()
def generate_bidder_signer():
 p=rsa.generate_private_key(public_exponent=65537,key_size=3072);return p,p.public_key()
def sign_bid(record,private):return private.sign(record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_bid(record,sig,public):
 try:public.verify(sig,record,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256());return True
 except (InvalidSignature,ValueError):return False
def generate_evaluator_keypair():
 p=x25519.X25519PrivateKey.generate();return p,p.public_key()
def encrypt_bid(data,public):
 e=x25519.X25519PrivateKey.generate();shared=e.exchange(public);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'tenderproof-bid-v1').derive(shared);n=os.urandom(12);return e.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),n,AESGCM(key).encrypt(n,data,b'tenderproof-bid-v1')
def decrypt_bid(env,private):
 ep,n,ct=env;shared=private.exchange(x25519.X25519PublicKey.from_public_bytes(ep));key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'tenderproof-bid-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,ct,b'tenderproof-bid-v1')
 except InvalidTag as e:raise ValueError('bid package authentication failed') from e
def export_bidder_key(public):return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_bidder_key(raw):
 p=serialization.load_pem_public_key(raw)
 if not isinstance(p,rsa.RSAPublicKey):raise ValueError('expected RSA bidder key')
 return p

def load_evaluator_key(raw):return x25519.X25519PublicKey.from_public_bytes(raw)
def export_evaluator_key(private_public):return private_public.public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
