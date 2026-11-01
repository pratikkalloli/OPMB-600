"""Canonical event-pass data and RSA-PSS baseline."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def canonical_pass(pass_id: str, event_id: str, holder_alias: str, serial: int, expires_at: int) -> bytes:
    if not all((pass_id, event_id, holder_alias)) or serial < 1 or expires_at <= 0:
        raise ValueError("invalid pass fields")
    value = {"pass_id": pass_id, "event_id": event_id, "holder_alias": holder_alias,
             "serial": serial, "expires_at": expires_at, "format": 1}
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def generate_signer():
    private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private, private.public_key()


def sign_pass(payload: bytes, private) -> bytes:
    return private.sign(payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                         salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())


def verify_pass(payload: bytes, signature: bytes, public) -> bool:
    try:
        public.verify(signature, payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                      salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except (InvalidSignature, ValueError):
        return False


def export_public_key(public) -> bytes:
    return public.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)


def load_public_key(encoded: bytes):
    key = serialization.load_pem_public_key(encoded)
    if not isinstance(key, rsa.RSAPublicKey):
        raise ValueError("expected RSA pass issuer key")
    return key
