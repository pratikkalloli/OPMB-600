"""PQC reference for two-person payment approval and desk transfers."""
import json,os
from dataclasses import dataclass
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
@dataclass(frozen=True)
class Approval:
    instruction_id:str; approver:str; amount_minor:int; currency:str; beneficiary:str; signature:bytes
def canonical_instruction(iid,amount_minor,currency,beneficiary):
    if not iid or amount_minor<1 or len(currency)!=3 or not currency.isalpha() or not beneficiary: raise ValueError('invalid payment instruction')
    return json.dumps({'id':iid,'amount_minor':amount_minor,'currency':currency.upper(),'beneficiary':beneficiary},sort_keys=True,separators=(',',':')).encode()
def generate_approver(): return mldsa.MLDSA65PrivateKey.generate()
def sign_approval(payload,private): return private.sign(payload,context=b'clearing-approval-v1')
def verify_approval(payload,signature,public):
    try: public.verify(signature,payload,context=b'clearing-approval-v1'); return True
    except (InvalidSignature,ValueError): return False
def export_approver(public): return public.public_bytes_raw()
def load_approver(raw): return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
def generate_desk_keypair():
    p=mlkem.MLKEM768PrivateKey.generate(); return p,p.public_key()
def seal_transfer(payload,recipient_public):
    shared,ct=recipient_public.encapsulate(); key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'clearing-transfer-v1').derive(shared); nonce=os.urandom(12); return ct,nonce,AESGCM(key).encrypt(nonce,payload,b'clearing-transfer-v1')
def open_transfer(envelope,recipient_private):
    ct,nonce,ciphertext=envelope; shared=recipient_private.decapsulate(ct); key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'clearing-transfer-v1').derive(shared)
    try: return AESGCM(key).decrypt(nonce,ciphertext,b'clearing-transfer-v1')
    except InvalidTag as e: raise ValueError('transfer authentication failed') from e
