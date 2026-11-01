"""Classical RSA-PSS and RSA-OAEP/AES-GCM operations."""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, json, base64
from .domain import canonical_record

CONTEXT = b"OPMB-600/inverter_protection_profile/record/v1"
def generate_signer(): return rsa.generate_private_key(public_exponent=65537, key_size=3072)
def sign_record(record, private): return private.sign(CONTEXT + b"\0" + canonical_record(record), padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
def verify_record(record, signature, public):
    try: public.verify(signature, CONTEXT + b"\0" + canonical_record(record), padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256()); return True
    except (InvalidSignature, ValueError, TypeError): return False
def export_public_key(public): return public.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
def load_public_key(data):
    key=serialization.load_pem_public_key(data)
    if not isinstance(key, rsa.RSAPublicKey): raise ValueError("expected RSA verification key")
    return key
def seal_artifact(payload: bytes, recipient):
    key=os.urandom(32); nonce=os.urandom(12); aad=b"OPMB-600/inverter_protection_profile/artifact/v1"
    ciphertext=AESGCM(key).encrypt(nonce,payload,aad)
    wrapped=recipient.encrypt(key,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=aad))
    return json.dumps({"v":1,"alg":"RSA-OAEP+AES-256-GCM","nonce":base64.b64encode(nonce).decode(),"key":base64.b64encode(wrapped).decode(),"ct":base64.b64encode(ciphertext).decode()},sort_keys=True,separators=(",",":")).encode()
def open_artifact(envelope: bytes, private):
    try:
        obj=json.loads(envelope); assert obj["v"]==1 and obj["alg"]=="RSA-OAEP+AES-256-GCM"
        aad=b"OPMB-600/inverter_protection_profile/artifact/v1"; nonce=base64.b64decode(obj["nonce"],validate=True); wrapped=base64.b64decode(obj["key"],validate=True); ct=base64.b64decode(obj["ct"],validate=True)
        if len(nonce)!=12: raise ValueError("bad nonce")
        key=private.decrypt(wrapped,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=aad))
        if len(key)!=32: raise ValueError("bad data key")
        return AESGCM(key).decrypt(nonce,ct,aad)
    except Exception as exc: raise ValueError("invalid or unauthenticated artifact envelope") from exc
