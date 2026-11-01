"""FIPS 204 pass signing and serialization."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa


def canonical_pass(pass_id: str, event_id: str, holder_alias: str, serial: int, expires_at: int) -> bytes:
    if not all((pass_id, event_id, holder_alias)) or serial < 1 or expires_at <= 0:
        raise ValueError("invalid pass fields")
    value = {"pass_id": pass_id, "event_id": event_id, "holder_alias": holder_alias,
             "serial": serial, "expires_at": expires_at, "format": 1}
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def generate_signer():
    return mldsa.MLDSA65PrivateKey.generate()


def sign_pass(payload: bytes, private) -> bytes:
    return private.sign(payload, context=b"eventpass-credential-v1")


def verify_pass(payload: bytes, signature: bytes, public) -> bool:
    try:
        public.verify(signature, payload, context=b"eventpass-credential-v1")
        return True
    except (InvalidSignature, ValueError):
        return False


def export_public_key(public) -> bytes:
    return public.public_bytes_raw()


def load_public_key(encoded: bytes):
    return mldsa.MLDSA65PublicKey.from_public_bytes(encoded)
