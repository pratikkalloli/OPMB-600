"""SessionExchange domain workflows for secure session establishment and negotiation."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class SessionOfferRecord(TypedDict):
    session_id: str
    initiator: str
    responder: str
    offered_suites: list[Any]
    nonce: str
    transcript_hash: str

CONTEXT = b"opmb-600:sessionexchange:v1"
REQUIRED_FIELDS = ['session_id', 'initiator', 'responder', 'offered_suites', 'nonce', 'transcript_hash']

def create_session_offer_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_session_offer_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_session_offer_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_session_offer(record: SessionOfferRecord) -> SessionOfferRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required session_offer fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported session_offer fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required session_offer fields cannot be empty")
    try:
        if not record['offered_suites']: raise ValueError('at least one suite must be offered')
        if record['initiator'] == record['responder']: raise ValueError('session peers must be distinct')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed session_offer domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc
    suites = normalized["offered_suites"]
    if not isinstance(suites, list) or not suites or not all(isinstance(x, str) for x in suites) or len(suites) != len(set(suites)):
        raise ValueError("offered suites must be a non-empty list of unique strings")
    return normalized

def canonicalize_session_offer(record: SessionOfferRecord) -> bytes:
    normalized = validate_session_offer(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_session_offer(identity: dict, record: SessionOfferRecord) -> bytes:
    payload = canonicalize_session_offer(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_session_offer(public_key, record: SessionOfferRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_session_offer(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_session_offer_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_session_offer_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_session_offer_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_session_offer_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)
def negotiate_session_suite(record: dict, supported_suites: list[str]) -> str:
    offered = validate_session_offer(record)["offered_suites"]
    selected = next((suite for suite in offered if suite in supported_suites), None)
    if selected is None:
        raise ValueError("no mutually supported session suite")
    return selected

class SessionExchangeLedger:
    """SQLite-backed append-only ledger for validated, signed session offers."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: SessionOfferRecord) -> None:
        return
    def publish(self, identity: dict, record: SessionOfferRecord) -> bytes:
        normalized = validate_session_offer(record)
        record_id = str(record['session_id'])
        if record_id is None or not str(record_id).strip():
            raise ValueError("session_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_session_offer(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate session_offer identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_sessionexchange_workflow(identity: dict, record: SessionOfferRecord, ledger: SessionExchangeLedger | None = None) -> dict:
    normalized = validate_session_offer(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_session_offer(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> SessionOfferRecord:
    return json.loads('{"initiator":"client-1","nonce":"cccccccccccccccccccccccccccccccc","offered_suites":["ML-KEM-768+A256GCM"],"responder":"gateway-1","session_id":"sess-001","transcript_hash":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"}')
