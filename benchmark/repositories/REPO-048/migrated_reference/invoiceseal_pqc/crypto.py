"""FIPS 204 invoice signature operations."""
from __future__ import annotations

import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa


def canonical_invoice(invoice_id: str, issuer: str, amount_minor: int, currency: str, revision: int) -> bytes:
    if not invoice_id or not issuer or amount_minor < 0 or len(currency) != 3 or revision < 1:
        raise ValueError("invalid synthetic invoice fields")
    fields = {"invoice_id": invoice_id, "issuer": issuer, "amount_minor": amount_minor,
              "currency": currency.upper(), "revision": revision}
    return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()


def generate_signer():
    return mldsa.MLDSA65PrivateKey.generate()


def sign_invoice(payload: bytes, private) -> bytes:
    return private.sign(payload, context=b"invoiceseal-invoice-v1")


def verify_invoice(payload: bytes, signature: bytes, public) -> bool:
    try:
        public.verify(signature, payload, context=b"invoiceseal-invoice-v1")
        return True
    except (InvalidSignature, ValueError):
        return False


def export_public_key(public) -> bytes:
    return public.public_bytes_raw()


def load_public_key(raw: bytes):
    return mldsa.MLDSA65PublicKey.from_public_bytes(raw)


def invoice_digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def signature_id(invoice_id: str, issuer: str, revision: int, algorithm: str = "ML-DSA-65") -> str:
    if not invoice_id or not issuer or revision < 1:
        raise ValueError("invalid invoice signature identity")
    return hashlib.sha256(f"{algorithm}:{issuer}:{invoice_id}:{revision}".encode()).hexdigest()[:32]
