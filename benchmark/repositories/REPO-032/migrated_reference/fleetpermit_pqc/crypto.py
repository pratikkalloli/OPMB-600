"""FleetPermit cryptographic primitives; FIPS 203/204."""
from __future__ import annotations
import base64, json, os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa

VERSION = 1
SIGNATURE_ALGORITHM = "ML-DSA-65"
ENVELOPE_ALGORITHM = "ML-KEM-768+HKDF-SHA256+AES-256-GCM"
SIGNING_PRIVATE = mldsa.MLDSA65PrivateKey
SIGNING_PUBLIC = mldsa.MLDSA65PublicKey
TRANSPORT_PRIVATE = mlkem.MLKEM768PrivateKey
TRANSPORT_PUBLIC = mlkem.MLKEM768PublicKey

def generate_signing_keypair():
    private = mldsa.MLDSA65PrivateKey.generate()
    return private, private.public_key()

def generate_transport_keypair():
    private = mlkem.MLKEM768PrivateKey.generate()
    return private, private.public_key()

def serialize_public_key(public, purpose: str) -> bytes:
    if not isinstance(public, (SIGNING_PUBLIC, TRANSPORT_PUBLIC)):
        raise ValueError("unsupported public-key type")
    expected = {"signing": SIGNING_PUBLIC, "transport": TRANSPORT_PUBLIC}.get(purpose)
    if expected is None or not isinstance(public, expected):
        raise ValueError("public-key algorithm does not match its purpose")
    der = public.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return json.dumps({"v": VERSION, "purpose": purpose, "key": base64.b64encode(der).decode()}, sort_keys=True, separators=(",", ":")).encode()

def load_public_key(encoded: bytes, purpose: str):
    if not isinstance(encoded, bytes) or not encoded:
        raise ValueError("encoded public key must be non-empty bytes")
    try:
        obj = json.loads(encoded)
        if set(obj) != {"v", "purpose", "key"} or obj["v"] != VERSION or obj["purpose"] != purpose:
            raise ValueError("public-key purpose or version mismatch")
        der = base64.b64decode(obj["key"], validate=True)
        key = serialization.load_der_public_key(der)
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError("malformed or purpose-mismatched public key") from exc
    expected = {"signing": SIGNING_PUBLIC, "transport": TRANSPORT_PUBLIC}.get(purpose)
    if expected is None or not isinstance(key, expected):
        raise ValueError("public-key algorithm does not match its purpose")
    return key

def sign_document(payload: bytes, private, context: bytes) -> bytes:
    if not isinstance(payload, bytes) or not payload or not isinstance(context, bytes):
        raise ValueError("payload and byte context are required")
    if not isinstance(private, SIGNING_PRIVATE):
        raise ValueError("wrong signing private-key type")
    signature = private.sign(context + b'\x00' + payload)
    return json.dumps({"v": VERSION, "alg": SIGNATURE_ALGORITHM,
                       "payload": base64.b64encode(payload).decode(),
                       "signature": base64.b64encode(signature).decode()},
                      sort_keys=True, separators=(",", ":")).encode()

def verify_document(envelope: bytes, public, context: bytes):
    if not isinstance(public, SIGNING_PUBLIC) or not isinstance(context, bytes):
        return None
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "payload", "signature"} or obj["v"] != VERSION or obj["alg"] != SIGNATURE_ALGORITHM:
            return None
        payload = base64.b64decode(obj["payload"], validate=True)
        signature = base64.b64decode(obj["signature"], validate=True)
        public.verify(signature, context + b'\x00' + payload)
        return payload
    except (ValueError, TypeError, KeyError, InvalidSignature):
        return None

def seal_payload(plaintext: bytes, public, context: bytes) -> bytes:
    if not isinstance(plaintext, bytes) or not plaintext or not isinstance(context, bytes):
        raise ValueError("plaintext and byte context are required")
    if not isinstance(public, TRANSPORT_PUBLIC):
        raise ValueError("wrong transport public-key type")
    shared, enc = public.encapsulate(); key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'OPMB-600:fleetpermit:v1:' + context).derive(shared); wrapped = base64.b64encode(enc).decode()
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, context)
    return json.dumps({"v": VERSION, "alg": ENVELOPE_ALGORITHM, 'enc': wrapped, "nonce": base64.b64encode(nonce).decode(), "ciphertext": base64.b64encode(ciphertext).decode()}, sort_keys=True, separators=(",", ":")).encode()

def open_payload(envelope: bytes, private, context: bytes) -> bytes:
    if not isinstance(private, TRANSPORT_PRIVATE) or not isinstance(context, bytes):
        raise ValueError("wrong transport private-key type or context")
    try:
        obj = json.loads(envelope)
        if set(obj) != {'v', 'alg', 'enc', 'nonce', 'ciphertext'} or obj["v"] != VERSION or obj["alg"] != ENVELOPE_ALGORITHM:
            raise ValueError("unsupported envelope")
        nonce = base64.b64decode(obj["nonce"], validate=True)
        ciphertext = base64.b64decode(obj["ciphertext"], validate=True)
        if len(nonce) != 12:
            raise ValueError("invalid nonce length")
        enc = base64.b64decode(obj['enc'], validate=True)
        if len(enc) != 1088:
            raise ValueError('invalid ML-KEM-768 ciphertext length')
        shared = private.decapsulate(enc)
        key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'OPMB-600:fleetpermit:v1:' + context).derive(shared)

        return AESGCM(key).decrypt(nonce, ciphertext, context)
    except (ValueError, TypeError, KeyError, InvalidTag) as exc:
        raise ValueError("invalid, modified, or context-mismatched envelope") from exc

class KeyRegistry:
    """In-memory versioned identities with final revocation semantics."""
    def __init__(self):
        self._entries = {}
    def provision(self, key_id: str):
        if not isinstance(key_id, str) or not key_id.strip() or key_id in self._entries:
            raise ValueError("invalid or duplicate key identifier")
        signing_private, signing_public = generate_signing_keypair()
        transport_private, transport_public = generate_transport_keypair()
        entry = {"version": 1, "status": "active", "signing_private": signing_private,
                 "signing_public": signing_public, "transport_private": transport_private,
                 "transport_public": transport_public}
        self._entries[key_id] = entry
        return self._public_view(entry)
    def rotate(self, key_id: str):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active":
            raise ValueError("key is unavailable or revoked")
        signing_private, signing_public = generate_signing_keypair()
        transport_private, transport_public = generate_transport_keypair()
        entry = {"version": old["version"] + 1, "status": "active",
                 "signing_private": signing_private, "signing_public": signing_public,
                 "transport_private": transport_private, "transport_public": transport_public}
        self._entries[key_id] = entry
        return self._public_view(entry)
    def revoke(self, key_id: str):
        entry = self._entries.get(key_id)
        if not entry or entry["status"] != "active":
            raise ValueError("key is unavailable or already revoked")
        self._entries[key_id] = {"version": entry["version"], "status": "revoked"}
    def get_active(self, key_id: str, version: int):
        entry = self._entries.get(key_id)
        if not entry or entry["status"] != "active" or entry["version"] != version:
            raise ValueError("unknown, revoked, or stale key version")
        return dict(entry)
    @staticmethod
    def _public_view(entry):
        return {"version": entry["version"],
                "signing_public": serialize_public_key(entry["signing_public"], "signing"),
                "transport_public": serialize_public_key(entry["transport_public"], "transport")}
