"""Separate FIPS 203 ML-KEM and FIPS 204 ML-DSA reference operations."""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa, mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os, json, base64
from .domain import canonical_record

CONTEXT=b"OPMB-600/renewable_output_certificate/record/v1"
AAD=b"OPMB-600/renewable_output_certificate/artifact/v1"
def generate_signer(): return mldsa.MLDSA65PrivateKey.generate()
def sign_record(record, private): return private.sign(CONTEXT+b"\0"+canonical_record(record), context=b"opmb600-renewable_output_certificate-v1")
def verify_record(record, signature, public):
    try: public.verify(signature, CONTEXT+b"\0"+canonical_record(record), context=b"opmb600-renewable_output_certificate-v1"); return True
    except (InvalidSignature, ValueError, TypeError): return False
def export_public_key(public): return b"MLDSA65v1:"+public.public_bytes_raw()
def load_public_key(data):
    if not data.startswith(b"MLDSA65v1:"): raise ValueError("unknown verification key version")
    return mldsa.MLDSA65PublicKey.from_public_bytes(data[len(b"MLDSA65v1:"):])
def generate_recipient(): return mlkem.MLKEM768PrivateKey.generate()
def seal_artifact(payload: bytes, recipient_public):
    shared, encapsulation=recipient_public.encapsulate()
    key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=AAD+encapsulation).derive(shared)
    nonce=os.urandom(12); ciphertext=AESGCM(key).encrypt(nonce,payload,AAD+encapsulation)
    return json.dumps({"v":1,"kem":"ML-KEM-768","aead":"AES-256-GCM","enc":base64.b64encode(encapsulation).decode(),"nonce":base64.b64encode(nonce).decode(),"ct":base64.b64encode(ciphertext).decode()},sort_keys=True,separators=(",",":")).encode()
def open_artifact(envelope: bytes, recipient_private):
    try:
        obj=json.loads(envelope); assert obj["v"]==1 and obj["kem"]=="ML-KEM-768" and obj["aead"]=="AES-256-GCM"
        enc=base64.b64decode(obj["enc"],validate=True); nonce=base64.b64decode(obj["nonce"],validate=True); ct=base64.b64decode(obj["ct"],validate=True)
        if len(nonce)!=12: raise ValueError("bad nonce")
        shared=recipient_private.decapsulate(enc); key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=AAD+enc).derive(shared)
        return AESGCM(key).decrypt(nonce,ct,AAD+enc)
    except Exception as exc: raise ValueError("invalid or unauthenticated artifact envelope") from exc
