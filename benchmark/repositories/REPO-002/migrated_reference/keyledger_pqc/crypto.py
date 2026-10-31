"""FIPS 203/204 KeyLedger reference operations."""
from __future__ import annotations
import hashlib,os
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import mlkem,mldsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
def generate_signing_keypair():
 p=mldsa.MLDSA65PrivateKey.generate(); return p,p.public_key()
def generate_transport_keypair():
 p=mlkem.MLKEM768PrivateKey.generate(); return p,p.public_key()
def serialize_public_key(public): return public.public_bytes_raw()
def load_public_key(raw): return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
def serialize_private_key(private,password:bytes):
 if not password: raise ValueError("a nonempty storage password is required")
 return private.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.BestAvailableEncryption(password))
def load_private_key(data:bytes,password:bytes):
 key=serialization.load_pem_private_key(data,password=password)
 if not isinstance(key,(mlkem.MLKEM768PrivateKey,mldsa.MLDSA65PrivateKey)): raise ValueError("unsupported PQC private-key type")
 return key
def sign_audit_event(event:bytes,private): return private.sign(event,context=b"keyledger-audit-v1")
def verify_audit_event(event:bytes,signature:bytes,public)->bool:
 try: public.verify(signature,event,context=b"keyledger-audit-v1"); return True
 except (InvalidSignature,ValueError): return False
def wrap_recovery_secret(secret:bytes,public,*,key_id:str):
 if not secret or not key_id: raise ValueError("secret and key ID are required")
 shared,ct=public.encapsulate(); kek=HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(b"keyledger:pqc:v1").digest(),info=key_id.encode()).derive(shared); nonce=os.urandom(12); return ct+nonce+AESGCM(kek).encrypt(nonce,secret,key_id.encode())
def unwrap_recovery_secret(envelope:bytes,private,*,key_id:str):
 if len(envelope)<1088+12+16: raise ValueError("invalid recovery envelope")
 ct,nonce,wrapped=envelope[:1088],envelope[1088:1100],envelope[1100:]; shared=private.decapsulate(ct); kek=HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(b"keyledger:pqc:v1").digest(),info=key_id.encode()).derive(shared)
 try: return AESGCM(kek).decrypt(nonce,wrapped,key_id.encode())
 except (ValueError,InvalidTag) as e: raise ValueError("recovery envelope authentication failed") from e
def public_key_fingerprint(public)->str: return hashlib.sha256(public.public_bytes_raw()).hexdigest()
