"""TrustBridge synthetic reference using FIPS 203 ML-KEM and FIPS 204 ML-DSA."""
from __future__ import annotations
import base64, hashlib, json, os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

VERSION = 1
SIGNING_ALGORITHM = "ML-DSA-65"
KEM_ALGORITHM = "ML-KEM-768"

def generate_signing_keypair():
    private = mldsa.MLDSA65PrivateKey.generate(); return private, private.public_key()

def generate_kem_keypair():
    private = mlkem.MLKEM768PrivateKey.generate(); return private, private.public_key()

def serialize_public_key(key) -> bytes:
    if not isinstance(key, (mldsa.MLDSA65PublicKey, mlkem.MLKEM768PublicKey)):
        raise ValueError("unsupported public key type")
    return key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)

def load_public_key(data: bytes, purpose: str):
    try: key = serialization.load_der_public_key(data)
    except (ValueError, TypeError) as exc: raise ValueError("malformed public key") from exc
    expected = {"signature": mldsa.MLDSA65PublicKey, "kem": mlkem.MLKEM768PublicKey}.get(purpose)
    if expected is None or not isinstance(key, expected): raise ValueError("public key algorithm does not match purpose")
    return key

class KeyRegistry:
    """Small in-memory versioned registry; revocation is final for each key id."""
    def __init__(self): self._entries = {}
    def provision(self, key_id: str):
        if not isinstance(key_id, str) or not key_id.strip() or key_id in self._entries: raise ValueError("invalid or duplicate key identifier")
        signing_private, signing_public = generate_signing_keypair()
        kem_private, kem_public = generate_kem_keypair()
        entry = {"version": VERSION, "status": "active", "signing_private": signing_private, "signing_public": signing_public, "kem_private": kem_private, "kem_public": kem_public}
        self._entries[key_id] = entry
        return {"version": VERSION, "signing_public": serialize_public_key(signing_public), "kem_public": serialize_public_key(kem_public)}
    def rotate(self, key_id: str):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active": raise ValueError("key is unavailable or revoked")
        replacement = {"version": old["version"] + 1, "status": "active", "signing_private": generate_signing_keypair()[0], "kem_private": generate_kem_keypair()[0]}
        replacement["signing_public"] = replacement["signing_private"].public_key(); replacement["kem_public"] = replacement["kem_private"].public_key()
        self._entries[key_id] = replacement
        return {"version": replacement["version"], "signing_public": serialize_public_key(replacement["signing_public"]), "kem_public": serialize_public_key(replacement["kem_public"])}
    def revoke(self, key_id: str):
        if key_id not in self._entries or self._entries[key_id]["status"] != "active": raise ValueError("key is unavailable or already revoked")
        self._entries[key_id] = {"version": self._entries[key_id]["version"], "status": "revoked"}
    def get_active(self, key_id: str, version: int):
        entry = self._entries.get(key_id)
        if not entry or entry["status"] != "active" or version != entry["version"]: raise ValueError("unknown, revoked, or stale key version")
        return entry

def _sign(payload: bytes, key, context: bytes) -> bytes:
    if not isinstance(key, mldsa.MLDSA65PrivateKey): raise ValueError("ML-DSA-65 private key required")
    signed = context + b"\x00" + payload
    return json.dumps({"v": VERSION, "alg": SIGNING_ALGORITHM, "payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(key.sign(signed)).decode()}, sort_keys=True, separators=(",", ":")).encode()

def _verify(envelope: bytes, key, context: bytes) -> bool:
    if not isinstance(key, mldsa.MLDSA65PublicKey): return False
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "payload", "signature"} or obj["v"] != VERSION or obj["alg"] != SIGNING_ALGORITHM: return False
        payload = base64.b64decode(obj["payload"], validate=True); signature = base64.b64decode(obj["signature"], validate=True)
        key.verify(signature, context + b"\x00" + payload); return True
    except (ValueError, TypeError, KeyError, InvalidSignature): return False

def _encrypt(payload: bytes, public, context: bytes) -> bytes:
    if not isinstance(public, mlkem.MLKEM768PublicKey): raise ValueError("ML-KEM-768 public key required")
    shared, encapsulation = public.encapsulate()
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"OPMB TrustBridge v1\x00" + context).derive(shared)
    nonce = os.urandom(12); ciphertext = AESGCM(key).encrypt(nonce, payload, context)
    return json.dumps({"v": VERSION, "alg": KEM_ALGORITHM, "enc": base64.b64encode(encapsulation).decode(), "nonce": base64.b64encode(nonce).decode(), "ciphertext": base64.b64encode(ciphertext).decode()}, sort_keys=True, separators=(",", ":")).encode()

def _decrypt(envelope: bytes, private, context: bytes) -> bytes:
    if not isinstance(private, mlkem.MLKEM768PrivateKey): raise ValueError("ML-KEM-768 private key required")
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "enc", "nonce", "ciphertext"} or obj["v"] != VERSION or obj["alg"] != KEM_ALGORITHM: raise ValueError
        enc, nonce, ciphertext = (base64.b64decode(obj[x], validate=True) for x in ("enc", "nonce", "ciphertext"))
        if len(enc) != 1088 or len(nonce) != 12: raise ValueError
        shared = private.decapsulate(enc)
        key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"OPMB TrustBridge v1\x00" + context).derive(shared)
        return AESGCM(key).decrypt(nonce, ciphertext, context)
    except (ValueError, TypeError, KeyError, InvalidTag) as exc: raise ValueError("invalid or modified PQC envelope") from exc

def operation(number, private_key, public_key, payload: bytes, context: bytes = b"opmb-v1"):
    if not isinstance(payload, bytes) or not payload: raise ValueError("payload must be non-empty bytes")
    if number in (5, 6, 7):
        if private_key is not None:
            kem_public = private_key.public_key() if isinstance(private_key, mlkem.MLKEM768PrivateKey) else private_key
            return _encrypt(payload, kem_public, context)
        return _decrypt(payload, public_key, context)
    return _sign(payload, private_key, context) if private_key is not None else _verify(payload, public_key, context)

def operation_01(private_key, public_key, payload, context=b"opmb-v1"): return operation(1, private_key, public_key, payload, context)
def operation_02(private_key, public_key, payload, context=b"opmb-v1"): return operation(2, private_key, public_key, payload, context)
def operation_03(private_key, public_key, payload, context=b"opmb-v1"): return operation(3, private_key, public_key, payload, context)
def operation_04(private_key, public_key, payload, context=b"opmb-v1"): return operation(4, private_key, public_key, payload, context)
def operation_05(private_key, public_key, payload, context=b"opmb-v1"): return operation(5, private_key, public_key, payload, context)
def operation_06(private_key, public_key, payload, context=b"opmb-v1"): return operation(6, private_key, public_key, payload, context)
def operation_07(private_key, public_key, payload, context=b"opmb-v1"): return operation(7, private_key, public_key, payload, context)
def operation_08(private_key, public_key, payload, context=b"opmb-v1"): return operation(8, private_key, public_key, payload, context)
def operation_09(private_key, public_key, payload, context=b"opmb-v1"): return operation(9, private_key, public_key, payload, context)
def operation_10(private_key, public_key, payload, context=b"opmb-v1"): return operation(10, private_key, public_key, payload, context)
