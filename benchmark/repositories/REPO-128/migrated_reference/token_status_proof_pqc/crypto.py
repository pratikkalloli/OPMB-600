"""FIPS 203 ML-KEM and FIPS 204 ML-DSA primitives for TokenStatusProof."""
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
SIGNING_PRIVATE, SIGNING_PUBLIC = mldsa.MLDSA65PrivateKey, mldsa.MLDSA65PublicKey
TRANSPORT_PRIVATE, TRANSPORT_PUBLIC = mlkem.MLKEM768PrivateKey, mlkem.MLKEM768PublicKey
CONTEXT = b"opmb-scale600:token_status_proof:v1"

def generate_signing_keypair():
    private = SIGNING_PRIVATE.generate()
    return private, private.public_key()

def generate_transport_keypair():
    private = TRANSPORT_PRIVATE.generate()
    return private, private.public_key()

def _expected(purpose):
    return {"signing": SIGNING_PUBLIC, "transport": TRANSPORT_PUBLIC}.get(purpose)

def serialize_public_key(public, purpose: str) -> bytes:
    expected = _expected(purpose)
    if expected is None or not isinstance(public, expected):
        raise ValueError("public key type does not match declared purpose")
    der = public.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return json.dumps({"v": VERSION, "purpose": purpose, "key": base64.b64encode(der).decode()}, sort_keys=True, separators=(",", ":")).encode()

def load_public_key(encoded: bytes, purpose: str):
    expected = _expected(purpose)
    if not isinstance(encoded, bytes) or not encoded or expected is None:
        raise ValueError("non-empty key bytes and a supported purpose are required")
    try:
        obj = json.loads(encoded)
        if set(obj) != {"v", "purpose", "key"} or obj["v"] != VERSION or obj["purpose"] != purpose:
            raise ValueError("key purpose or version mismatch")
        key = serialization.load_der_public_key(base64.b64decode(obj["key"], validate=True))
        if not isinstance(key, expected):
            raise ValueError("key algorithm does not match purpose")
        return key
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError("malformed or purpose-mismatched public key") from exc

def sign_document(payload: bytes, private, context: bytes) -> bytes:
    if not isinstance(payload, bytes) or not payload or not isinstance(context, bytes) or not isinstance(private, SIGNING_PRIVATE):
        raise ValueError("non-empty payload, byte context, and ML-DSA private key are required")
    signature = private.sign(context + b"\x00" + payload)
    return json.dumps({"v": VERSION, "alg": SIGNATURE_ALGORITHM, "payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True, separators=(",", ":")).encode()

def verify_document(envelope: bytes, public, context: bytes):
    if not isinstance(public, SIGNING_PUBLIC) or not isinstance(context, bytes):
        return None
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "payload", "signature"} or obj["v"] != VERSION or obj["alg"] != SIGNATURE_ALGORITHM:
            return None
        payload = base64.b64decode(obj["payload"], validate=True)
        public.verify(base64.b64decode(obj["signature"], validate=True), context + b"\x00" + payload)
        return payload
    except (ValueError, TypeError, KeyError, InvalidSignature):
        return None

def seal_payload(plaintext: bytes, public, context: bytes) -> bytes:
    if not isinstance(plaintext, bytes) or not plaintext or not isinstance(context, bytes) or not isinstance(public, TRANSPORT_PUBLIC):
        raise ValueError("non-empty plaintext, byte context, and ML-KEM public key are required")
    shared, encapsulation = public.encapsulate()
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=CONTEXT + b":" + context).derive(shared)
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, context)
    return json.dumps({"v": VERSION, "alg": ENVELOPE_ALGORITHM, "enc": base64.b64encode(encapsulation).decode(), "nonce": base64.b64encode(nonce).decode(), "ciphertext": base64.b64encode(ciphertext).decode()}, sort_keys=True, separators=(",", ":")).encode()

def open_payload(envelope: bytes, private, context: bytes) -> bytes:
    if not isinstance(private, TRANSPORT_PRIVATE) or not isinstance(context, bytes):
        raise ValueError("ML-KEM private key and byte context are required")
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "enc", "nonce", "ciphertext"} or obj["v"] != VERSION or obj["alg"] != ENVELOPE_ALGORITHM:
            raise ValueError("unsupported envelope")
        encapsulation = base64.b64decode(obj["enc"], validate=True)
        nonce = base64.b64decode(obj["nonce"], validate=True)
        ciphertext = base64.b64decode(obj["ciphertext"], validate=True)
        if len(encapsulation) != 1088 or len(nonce) != 12:
            raise ValueError("invalid ML-KEM encapsulation or nonce length")
        shared = private.decapsulate(encapsulation)
        key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=CONTEXT + b":" + context).derive(shared)
        return AESGCM(key).decrypt(nonce, ciphertext, context)
    except (ValueError, TypeError, KeyError, InvalidTag) as exc:
        raise ValueError("malformed, modified, or context-mismatched envelope") from exc

class KeyRegistry:
    """Versioned identities; rotation retires earlier keys and revocation is terminal."""
    def __init__(self): self._entries = {}
    def provision(self, key_id):
        if not isinstance(key_id, str) or not key_id.strip() or key_id in self._entries: raise ValueError("invalid or duplicate key id")
        return self._replace(key_id, 1)
    def _replace(self, key_id, version):
        signing_private, signing_public = generate_signing_keypair()
        transport_private, transport_public = generate_transport_keypair()
        entry = {"version": version, "status": "active", "signing_private": signing_private, "signing_public": signing_public, "transport_private": transport_private, "transport_public": transport_public}
        self._entries[key_id] = entry
        return self._public_view(entry)
    def rotate(self, key_id):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active": raise ValueError("key is unavailable or revoked")
        return self._replace(key_id, old["version"] + 1)
    def revoke(self, key_id):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active": raise ValueError("key is unavailable or already revoked")
        self._entries[key_id] = {"version": old["version"], "status": "revoked"}
    def get_active(self, key_id, version):
        entry = self._entries.get(key_id)
        if not entry or entry["status"] != "active" or entry["version"] != version: raise ValueError("unknown, revoked, or stale key version")
        return dict(entry)
    @staticmethod
    def _public_view(entry):
        return {"version": entry["version"], "signing_public": serialize_public_key(entry["signing_public"], "signing"), "transport_public": serialize_public_key(entry["transport_public"], "transport")}
