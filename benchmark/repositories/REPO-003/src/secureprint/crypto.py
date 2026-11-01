"""Classical cryptography baseline for SecurePrint migration tasks."""
from __future__ import annotations
import json
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_printer_keypair():
    private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private, private.public_key()

def generate_audit_keypair():
    private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private, private.public_key()

def serialize_public_key(public_key) -> bytes:
    return public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)

def load_public_key(encoded: bytes):
    key = serialization.load_pem_public_key(encoded)
    if not isinstance(key, rsa.RSAPublicKey):
        raise ValueError("expected RSA public key")
    return key

def validate_job_fields(job_id: str, owner: str, printer_id: str, content: bytes) -> None:
    if not all(isinstance(value, str) and value.strip() for value in (job_id, owner, printer_id)):
        raise ValueError("job, owner, and printer identifiers are required")
    if not isinstance(content, bytes) or not content or len(content) > 2_000_000:
        raise ValueError("print content must be 1..2000000 bytes")

def encrypt_job_content(content: bytes, printer_public_key, job_id: str) -> dict:
    if not content:
        raise ValueError("content is required")
    key = AESGCM.generate_key(bit_length=256)
    nonce = __import__("os").urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, content, job_id.encode())
    wrapped = printer_public_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=b"secureprint:job-key:v1"))
    return {"nonce": nonce, "ciphertext": ciphertext, "wrapped_key": wrapped}

def decrypt_job_content(package: dict, printer_private_key, job_id: str) -> bytes:
    try:
        key = printer_private_key.decrypt(package["wrapped_key"], padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=b"secureprint:job-key:v1"))
        return AESGCM(key).decrypt(package["nonce"], package["ciphertext"], job_id.encode())
    except (KeyError, ValueError, InvalidTag) as exc:
        raise ValueError("invalid or modified print package") from exc

def canonical_metadata(job_id: str, owner: str, printer_id: str, nonce: bytes, ciphertext: bytes, wrapped_key: bytes) -> bytes:
    if not all(isinstance(v, str) and v for v in (job_id, owner, printer_id)):
        raise ValueError("metadata identifiers are required")
    return json.dumps({"job_id": job_id, "owner": owner, "printer_id": printer_id, "nonce": nonce.hex(), "ciphertext_sha256": __import__("hashlib").sha256(ciphertext).hexdigest(), "wrapped_key_sha256": __import__("hashlib").sha256(wrapped_key).hexdigest()}, sort_keys=True, separators=(",", ":")).encode()

def sign_job_metadata(metadata: bytes, private_key) -> bytes:
    return private_key.sign(metadata, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

def verify_job_metadata(metadata: bytes, signature: bytes, public_key) -> bool:
    try:
        public_key.verify(signature, metadata, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except (InvalidSignature, ValueError):
        return False

def serialize_job_package(package: dict) -> bytes:
    if not all(isinstance(package.get(key), bytes) for key in ("nonce", "ciphertext", "wrapped_key")) or len(package["nonce"]) != 12:
        raise ValueError("malformed encrypted job package")
    return json.dumps({key: package[key].hex() for key in ("nonce", "ciphertext", "wrapped_key")}, sort_keys=True).encode()

def deserialize_job_package(encoded: bytes) -> dict:
    try:
        value = json.loads(encoded)
        package = {key: bytes.fromhex(value[key]) for key in ("nonce", "ciphertext", "wrapped_key")}
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError("malformed encrypted job package") from exc
    if len(package["nonce"]) != 12 or not package["ciphertext"] or not package["wrapped_key"]:
        raise ValueError("malformed encrypted job package")
    return package
