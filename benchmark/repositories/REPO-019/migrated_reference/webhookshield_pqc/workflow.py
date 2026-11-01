"""WebhookShield domain workflows for signed webhook delivery and replay protection."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class DeliveryRecord(TypedDict):
    endpoint_id: str
    event_id: str
    nonce: str
    timestamp: int
    body: dict[str, Any]

CONTEXT = b"opmb-600:webhookshield:v1"
REQUIRED_FIELDS = ['endpoint_id', 'event_id', 'nonce', 'timestamp', 'body']

def create_delivery_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_delivery_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_delivery_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_delivery(record: DeliveryRecord) -> DeliveryRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required delivery fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported delivery fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required delivery fields cannot be empty")
    try:
        if not str(record['nonce']).strip(): raise ValueError('nonce is required')
        if not isinstance(record['body'], dict): raise ValueError('webhook body must be an object')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed delivery domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_delivery(record: DeliveryRecord) -> bytes:
    normalized = validate_delivery(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_delivery(identity: dict, record: DeliveryRecord) -> bytes:
    payload = canonicalize_delivery(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_delivery(public_key, record: DeliveryRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_delivery(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_delivery_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_delivery_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_delivery_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_delivery_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class WebhookShieldLedger:
    """SQLite-backed append-only ledger for validated, signed webhook deliveries."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: DeliveryRecord) -> None:
        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        if any(item["nonce"] == record["nonce"] for item in rows):
            raise ValueError("webhook nonce replay detected")
    def publish(self, identity: dict, record: DeliveryRecord) -> bytes:
        normalized = validate_delivery(record)
        record_id = str(record['event_id'])
        if record_id is None or not str(record_id).strip():
            raise ValueError("event_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_delivery(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate delivery identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_webhookshield_workflow(identity: dict, record: DeliveryRecord, ledger: WebhookShieldLedger | None = None) -> dict:
    normalized = validate_delivery(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_delivery(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> DeliveryRecord:
    return json.loads('{"body":{"invoice":"inv-123","kind":"invoice.paid"},"endpoint_id":"billing-hook","event_id":"evt-001","nonce":"n-001","timestamp":1893456000}')
