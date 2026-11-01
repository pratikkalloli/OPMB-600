"""Classical baseline for two-person payment approval."""
import json, os
from dataclasses import dataclass
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

@dataclass(frozen=True)
class Approval:
    instruction_id:str; approver:str; amount_minor:int; currency:str; beneficiary:str; signature:bytes

def canonical_instruction(iid,amount_minor,currency,beneficiary):
    if not iid or amount_minor<1 or len(currency)!=3 or not currency.isalpha() or not beneficiary: raise ValueError("invalid payment instruction")
    return json.dumps({'id':iid,'amount_minor':amount_minor,'currency':currency.upper(),'beneficiary':beneficiary},sort_keys=True,separators=(',',':')).encode()
def generate_approver():
    p=rsa.generate_private_key(public_exponent=65537,key_size=3072); return p,p.public_key()
def sign_approval(payload,private): return private.sign(payload,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_approval(payload,signature,public):
    try: public.verify(signature,payload,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256()); return True
    except (InvalidSignature,ValueError): return False
def export_approver(public): return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_approver(raw):
    k=serialization.load_pem_public_key(raw)
    if not isinstance(k,rsa.RSAPublicKey): raise ValueError('expected RSA approver key')
    return k
def generate_desk_keypair():
    p=x25519.X25519PrivateKey.generate(); return p,p.public_key()
def seal_transfer(payload,recipient_public):
    eph=x25519.X25519PrivateKey.generate(); shared=eph.exchange(recipient_public); key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'clearing-transfer-v1').derive(shared); nonce=os.urandom(12); ct=AESGCM(key).encrypt(nonce,payload,b'clearing-transfer-v1'); return eph.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),nonce,ct
def open_transfer(envelope,recipient_private):
    ep,nonce,ct=envelope; shared=recipient_private.exchange(x25519.X25519PublicKey.from_public_bytes(ep)); key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'clearing-transfer-v1').derive(shared)
    try: return AESGCM(key).decrypt(nonce,ct,b'clearing-transfer-v1')
    except InvalidTag as e: raise ValueError('transfer authentication failed') from e
