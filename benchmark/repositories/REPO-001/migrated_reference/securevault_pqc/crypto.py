"""FIPS 203/204 operations through cryptography 50.x."""
from __future__ import annotations
import hashlib
import os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import mldsa, mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class VaultCryptoError(ValueError):
    """Raised when migrated cryptographic inputs fail validation."""

def generate_recipient_keypair() -> tuple[mlkem.MLKEM768PrivateKey, mlkem.MLKEM768PublicKey]:
    """Generate the FIPS 203 ML-KEM-768 recipient key pair."""
    private=mlkem.MLKEM768PrivateKey.generate()
    return private, private.public_key()

def _wrapping_key(shared_secret: bytes, object_id: str) -> bytes:
    if not object_id:
        raise VaultCryptoError("object ID is required")
    return HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(b"securevault:pqc:v1").digest(),info=b"securevault:key-wrap:"+object_id.encode("utf-8")).derive(shared_secret)

def wrap_data_key(data_key: bytes, recipient: mlkem.MLKEM768PublicKey, *, object_id: str) -> bytes:
    """Encapsulate to ML-KEM and AEAD-wrap a 256-bit data key."""
    if len(data_key)!=32:
        raise VaultCryptoError("data key must be 32 bytes")
    shared_secret,encapsulation=recipient.encapsulate(); nonce=os.urandom(12)
    wrapped=AESGCM(_wrapping_key(shared_secret,object_id)).encrypt(nonce,data_key,object_id.encode())
    return encapsulation+nonce+wrapped

def unwrap_data_key(wrapped: bytes, recipient: mlkem.MLKEM768PrivateKey, *, object_id: str) -> bytes:
    """Decapsulate and authenticate an object data key."""
    if len(wrapped)!=1088+12+48:
        raise VaultCryptoError("wrapped key has invalid length")
    encapsulation,nonce,ciphertext=wrapped[:1088],wrapped[1088:1100],wrapped[1100:]
    try:
        shared=recipient.decapsulate(encapsulation)
        key=AESGCM(_wrapping_key(shared,object_id)).decrypt(nonce,ciphertext,object_id.encode())
    except (ValueError,InvalidTag) as exc:
        raise VaultCryptoError("wrapped key could not be opened") from exc
    if len(key)!=32:
        raise VaultCryptoError("unwrapped data key has invalid length")
    return key

def encrypt_blob(plaintext: bytes,data_key: bytes,*,object_id: str)->tuple[bytes,bytes]:
    if len(data_key)!=32 or not object_id: raise VaultCryptoError("invalid encryption parameters")
    nonce=os.urandom(12); return nonce,AESGCM(data_key).encrypt(nonce,plaintext,object_id.encode())

def decrypt_blob(nonce: bytes,ciphertext: bytes,data_key: bytes,*,object_id: str)->bytes:
    try: return AESGCM(data_key).decrypt(nonce,ciphertext,object_id.encode())
    except (ValueError,InvalidTag) as exc: raise VaultCryptoError("document authentication failed") from exc

def generate_signing_keypair()->tuple[mldsa.MLDSA65PrivateKey,mldsa.MLDSA65PublicKey]:
    """Generate FIPS 204 ML-DSA-65 keys for manifest signatures."""
    private=mldsa.MLDSA65PrivateKey.generate(); return private,private.public_key()

def sign_manifest(manifest: bytes,private: mldsa.MLDSA65PrivateKey)->bytes:
    return private.sign(manifest)

def verify_manifest(manifest: bytes,signature: bytes,public: mldsa.MLDSA65PublicKey)->bool:
    try: public.verify(signature,manifest); return True
    except (InvalidSignature,ValueError): return False

def serialize_public_key(public: mlkem.MLKEM768PublicKey)->bytes:
    return public.public_bytes_raw()

def load_public_key(raw: bytes)->mlkem.MLKEM768PublicKey:
    try: return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
    except (ValueError,TypeError) as exc: raise VaultCryptoError("invalid ML-KEM public key") from exc

def rotate_object_key(wrapped_key: bytes,old_private: mlkem.MLKEM768PrivateKey,new_public: mlkem.MLKEM768PublicKey,*,object_id: str)->bytes:
    """Rewrap the existing per-object key under a newly rotated recipient key."""
    clear=unwrap_data_key(wrapped_key,old_private,object_id=object_id)
    return wrap_data_key(clear,new_public,object_id=object_id)
