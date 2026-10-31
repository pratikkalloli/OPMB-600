"""Classical cryptography supporting KeyLedger lifecycle audit events."""
from __future__ import annotations
import hashlib
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa

def generate_signing_keypair():
    private=rsa.generate_private_key(public_exponent=65537,key_size=3072); return private,private.public_key()
def generate_transport_keypair():
    private=rsa.generate_private_key(public_exponent=65537,key_size=3072); return private,private.public_key()
def serialize_public_key(public):
    return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_public_key(data):
    key=serialization.load_pem_public_key(data)
    if not isinstance(key,rsa.RSAPublicKey): raise ValueError("expected RSA public key")
    return key
def serialize_private_key(private,password:bytes):
    if not password: raise ValueError("a nonempty storage password is required")
    return private.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.BestAvailableEncryption(password))
def load_private_key(data,password:bytes):
    key=serialization.load_pem_private_key(data,password=password)
    if not isinstance(key,rsa.RSAPrivateKey): raise ValueError("expected RSA private key")
    return key
def sign_audit_event(event:bytes,private):
    return private.sign(event,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def verify_audit_event(event:bytes,signature:bytes,public)->bool:
    try: public.verify(signature,event,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256()); return True
    except (InvalidSignature,ValueError): return False
def wrap_recovery_secret(secret:bytes,public):
    if not secret or len(secret)>318: raise ValueError("RSA-OAEP-SHA256 supports at most 318 secret bytes")
    return public.encrypt(secret,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=b"keyledger:recovery:v1"))
def unwrap_recovery_secret(ciphertext:bytes,private):
    return private.decrypt(ciphertext,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=b"keyledger:recovery:v1"))
def public_key_fingerprint(public)->str:
    der=public.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo); return hashlib.sha256(der).hexdigest()
