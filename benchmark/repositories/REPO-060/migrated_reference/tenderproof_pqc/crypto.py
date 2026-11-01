"""ML-DSA/ML-KEM reference for confidential procurement bids."""
import hashlib,json,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def canonical_bid(tender_id,bidder,bid_id,amount_minor,proposal,submitted_at):
 if not all((tender_id,bidder,bid_id,proposal)) or amount_minor<1 or submitted_at<0:raise ValueError('invalid bid')
 return json.dumps({'tender_id':tender_id,'bidder':bidder,'bid_id':bid_id,'amount_minor':amount_minor,'proposal_sha256':hashlib.sha256(proposal).hexdigest(),'submitted_at':submitted_at},sort_keys=True,separators=(',',':')).encode()
def generate_bidder_signer():return mldsa.MLDSA65PrivateKey.generate()
def sign_bid(record,private):return private.sign(record,context=b'tenderproof-bid-v1')
def verify_bid(record,sig,public):
 try:public.verify(sig,record,context=b'tenderproof-bid-v1');return True
 except (InvalidSignature,ValueError):return False
def generate_evaluator_keypair():
 p=mlkem.MLKEM768PrivateKey.generate();return p,p.public_key()
def encrypt_bid(data,public):
 shared,ct=public.encapsulate();key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'tenderproof-bid-v1').derive(shared);n=os.urandom(12);return ct,n,AESGCM(key).encrypt(n,data,b'tenderproof-bid-v1')
def decrypt_bid(env,private):
 ct,n,cipher=env;shared=private.decapsulate(ct);key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'tenderproof-bid-v1').derive(shared)
 try:return AESGCM(key).decrypt(n,cipher,b'tenderproof-bid-v1')
 except InvalidTag as e:raise ValueError('bid package authentication failed') from e
def export_bidder_key(public):return public.public_bytes_raw()
def load_bidder_key(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)

def load_evaluator_key(raw):return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
def export_evaluator_key(private_public):return private_public.public_bytes_raw()
