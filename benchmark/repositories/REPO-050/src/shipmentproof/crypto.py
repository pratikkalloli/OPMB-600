"""Handoff serialization, signatures, and event-chain digests."""
import hashlib
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def canonical_handoff(shipment: str, sequence: int, sender: str, recipient: str, location: str, at: int, previous: str) -> bytes:
    if not all((shipment, sender, recipient, location)) or sequence < 1 or at <= 0:
        raise ValueError("invalid handoff fields")
    return json.dumps({"shipment":shipment,"sequence":sequence,"sender":sender,"recipient":recipient,
                       "location":location,"at":at,"previous":previous,"format":1},
                      sort_keys=True,separators=(",",":")).encode()


def generate_signer():
    p = rsa.generate_private_key(public_exponent=65537, key_size=3072); return p, p.public_key()


def sign_handoff(payload: bytes, private) -> bytes:
    return private.sign(payload,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())


def verify_handoff(payload: bytes, signature: bytes, public) -> bool:
    try:
        public.verify(signature,payload,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256()); return True
    except (InvalidSignature,ValueError): return False


def export_public_key(public) -> bytes:
    return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)


def load_public_key(value: bytes):
    key=serialization.load_pem_public_key(value)
    if not isinstance(key,rsa.RSAPublicKey): raise ValueError("expected RSA custody signer")
    return key


def event_digest(payload: bytes, signature: bytes) -> str:
    return hashlib.sha256(payload+signature).hexdigest()
