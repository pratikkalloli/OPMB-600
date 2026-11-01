"""Canonical invoice payloads and classical signature operations."""
from __future__ import annotations

import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def canonical_invoice(invoice_id: str, issuer: str, amount_minor: int, currency: str, revision: int) -> bytes:
    if not invoice_id or not issuer or amount_minor < 0 or len(currency) != 3 or revision < 1:
        raise ValueError("invalid synthetic invoice fields")
    fields = {"invoice_id": invoice_id, "issuer": issuer, "amount_minor": amount_minor,
              "currency": currency.upper(), "revision": revision}
    return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()


def generate_signer():
    private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private, private.public_key()


def sign_invoice(payload: bytes, private) -> bytes:
    return private.sign(payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())


def verify_invoice(payload: bytes, signature: bytes, public) -> bool:
    try:
        public.verify(signature, payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                      salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except (InvalidSignature, ValueError):
        return False


def export_public_key(public) -> bytes:
    return public.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)


def load_public_key(pem: bytes):
    key = serialization.load_pem_public_key(pem)
    if not isinstance(key, rsa.RSAPublicKey):
        raise ValueError("invoice signer key must be RSA")
    return key


def invoice_digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def signature_id(invoice_id: str, issuer: str, revision: int, algorithm: str = "RSA-PSS") -> str:
    if not invoice_id or not issuer or revision < 1:
        raise ValueError("invalid invoice signature identity")
    source = f"{algorithm}:{issuer}:{invoice_id}:{revision}".encode()
    return hashlib.sha256(source).hexdigest()[:32]
