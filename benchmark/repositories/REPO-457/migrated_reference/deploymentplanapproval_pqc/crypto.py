import json
from cryptography.hazmat.primitives.asymmetric import mldsa

def canonical_claims(claims: dict) -> bytes:
    if not isinstance(claims, dict): raise TypeError("claims must be a mapping")
    return json.dumps(claims, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def generate_signer(): return mldsa.MLDSA65PrivateKey.generate()
def export_public_key(private) -> bytes: return private.public_key().public_bytes_raw()
def load_public_key(encoded: bytes):
    if not isinstance(encoded, bytes) or len(encoded) != 1952: raise ValueError("invalid ML-DSA-65 public key")
    return mldsa.MLDSA65PublicKey.from_public_bytes(encoded)
def sign_claims(claims: dict, private) -> bytes: return private.sign(canonical_claims(claims))
def verify_claims(claims: dict, signature: bytes, public) -> bool:
    try: public.verify(signature, canonical_claims(claims)); return True
    except Exception: return False
