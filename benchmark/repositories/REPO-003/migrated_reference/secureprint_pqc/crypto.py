"""FIPS-algorithm reference operations using cryptography 50.0.2."""
from __future__ import annotations
import hashlib, json, os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def generate_printer_keypair():
    private = mlkem.MLKEM768PrivateKey.generate()
    return private, private.public_key()

def generate_audit_keypair():
    private = mldsa.MLDSA65PrivateKey.generate()
    return private, private.public_key()

def serialize_public_key(public_key) -> bytes:
    return public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)

def load_public_key(encoded: bytes, purpose: str):
    key = serialization.load_pem_public_key(encoded)
    expected = mlkem.MLKEM768PublicKey if purpose == "kem" else mldsa.MLDSA65PublicKey
    if not isinstance(key, expected):
        raise ValueError("public key algorithm does not match purpose")
    return key

def encrypt_job_content(content: bytes, printer_public_key, job_id: str) -> dict:
    if not content or not job_id:
        raise ValueError("content and job identifier are required")
    shared_secret, encapsulation = printer_public_key.encapsulate()
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"OPMB SecurePrint content key v1\x00" + job_id.encode()).derive(shared_secret)
    nonce = os.urandom(12)
    return {"nonce": nonce, "ciphertext": AESGCM(key).encrypt(nonce, content, job_id.encode()), "encapsulation": encapsulation}

def decrypt_job_content(package: dict, printer_private_key, job_id: str) -> bytes:
    try:
        shared_secret = printer_private_key.decapsulate(package["encapsulation"])
        key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"OPMB SecurePrint content key v1\x00" + job_id.encode()).derive(shared_secret)
        return AESGCM(key).decrypt(package["nonce"], package["ciphertext"], job_id.encode())
    except (KeyError, ValueError, InvalidTag) as exc:
        raise ValueError("invalid or modified print package") from exc

def canonical_metadata(job_id, owner, printer_id, nonce, ciphertext, encapsulation):
    return json.dumps({"job_id": job_id, "owner": owner, "printer_id": printer_id, "nonce": nonce.hex(), "ciphertext_sha256": hashlib.sha256(ciphertext).hexdigest(), "encapsulation_sha256": hashlib.sha256(encapsulation).hexdigest()}, sort_keys=True, separators=(",", ":")).encode()

def sign_job_metadata(metadata: bytes, private_key) -> bytes:
    return private_key.sign(metadata)

def verify_job_metadata(metadata: bytes, signature: bytes, public_key) -> bool:
    try:
        public_key.verify(signature, metadata)
        return True
    except (InvalidSignature, ValueError):
        return False

def serialize_job_package(package: dict) -> bytes:
    if not all(isinstance(package.get(key), bytes) for key in ("nonce", "ciphertext", "encapsulation")) or len(package["nonce"]) != 12:
        raise ValueError("malformed encrypted job package")
    return json.dumps({key: package[key].hex() for key in ("nonce", "ciphertext", "encapsulation")}, sort_keys=True).encode()

def deserialize_job_package(encoded: bytes) -> dict:
    try:
        value = json.loads(encoded)
        package = {key: bytes.fromhex(value[key]) for key in ("nonce", "ciphertext", "encapsulation")}
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError("malformed encrypted job package") from exc
    if len(package["nonce"]) != 12 or not package["ciphertext"] or not package["encapsulation"]:
        raise ValueError("malformed encrypted job package")
    return package
