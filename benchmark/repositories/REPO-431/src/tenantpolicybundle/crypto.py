import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

def canonical_claims(claims: dict) -> bytes:
    if not isinstance(claims, dict): raise TypeError("claims must be a mapping")
    return json.dumps(claims, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def generate_signer():
    return ec.generate_private_key(ec.SECP256R1())

def export_public_key(private) -> bytes:
    return private.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)

def load_public_key(encoded: bytes):
    key=serialization.load_der_public_key(encoded)
    if not isinstance(key, ec.EllipticCurvePublicKey) or key.curve.name != "secp256r1": raise ValueError("expected a P-256 public key")
    return key

def sign_claims(claims: dict, private) -> bytes:
    return private.sign(canonical_claims(claims), ec.ECDSA(hashes.SHA256()))

def verify_claims(claims: dict, signature: bytes, public) -> bool:
    try: public.verify(signature, canonical_claims(claims), ec.ECDSA(hashes.SHA256())); return True
    except Exception: return False
