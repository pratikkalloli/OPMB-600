"""Classical cryptographic primitives used by the SecureVault workflow."""
from __future__ import annotations
import os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class VaultCryptoError(ValueError):
    """Raised when a cryptographic input cannot be processed safely."""

def generate_recipient_keypair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Create the recipient's RSA-3072 OAEP key pair."""
    private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private, private.public_key()

def wrap_data_key(data_key: bytes, recipient: rsa.RSAPublicKey) -> bytes:
    """Wrap one 256-bit object key using RSA-OAEP with SHA-256."""
    if len(data_key) != 32:
        raise VaultCryptoError("data key must be 32 bytes")
    return recipient.encrypt(data_key, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=b"securevault:v1"))

def unwrap_data_key(wrapped_key: bytes, recipient: rsa.RSAPrivateKey) -> bytes:
    """Unwrap an object key; normalize malformed key failures."""
    try:
        key = recipient.decrypt(wrapped_key, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=b"securevault:v1"))
    except ValueError as exc:
        raise VaultCryptoError("wrapped key could not be opened") from exc
    if len(key) != 32:
        raise VaultCryptoError("unwrapped data key has invalid length")
    return key

def encrypt_blob(plaintext: bytes, data_key: bytes, *, object_id: str) -> tuple[bytes, bytes]:
    """Encrypt a document using AES-256-GCM and bind its object ID as AAD."""
    if len(data_key) != 32 or not object_id:
        raise VaultCryptoError("invalid encryption parameters")
    nonce = os.urandom(12)
    return nonce, AESGCM(data_key).encrypt(nonce, plaintext, object_id.encode("utf-8"))

def decrypt_blob(nonce: bytes, ciphertext: bytes, data_key: bytes, *, object_id: str) -> bytes:
    """Authenticate and decrypt a stored document."""
    try:
        return AESGCM(data_key).decrypt(nonce, ciphertext, object_id.encode("utf-8"))
    except (ValueError, InvalidTag) as exc:
        raise VaultCryptoError("document authentication failed") from exc

def generate_signing_keypair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Create a distinct RSA-3072 key pair for vault audit manifests."""
    private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private, private.public_key()

def sign_manifest(manifest: bytes, private: rsa.RSAPrivateKey) -> bytes:
    """Sign canonical manifest bytes using RSA-PSS/SHA-256."""
    return private.sign(manifest, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

def verify_manifest(manifest: bytes, signature: bytes, public: rsa.RSAPublicKey) -> bool:
    """Return false for invalid signatures without leaking crypto exceptions."""
    try:
        public.verify(signature, manifest, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except (InvalidSignature, ValueError):
        return False

def serialize_public_key(public: rsa.RSAPublicKey) -> bytes:
    """Serialize a public key in stable SubjectPublicKeyInfo PEM form."""
    return public.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)

def load_public_key(pem: bytes) -> rsa.RSAPublicKey:
    """Load and type-check a PEM public key."""
    try:
        key = serialization.load_pem_public_key(pem)
    except (ValueError, TypeError) as exc:
        raise VaultCryptoError("invalid public key encoding") from exc
    if not isinstance(key, rsa.RSAPublicKey):
        raise VaultCryptoError("expected an RSA public key")
    return key
