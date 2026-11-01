"""GeoDispatch domain workflows for protected dispatch instructions and signed location records."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class DispatchInstructionRecord(TypedDict):
    dispatch_id: str
    vehicle_id: str
    destination: dict[str, Any]
    issued_at: int
    expires_at: int

CONTEXT = b"opmb-600:geodispatch:v1"
REQUIRED_FIELDS = ['dispatch_id', 'vehicle_id', 'destination', 'issued_at', 'expires_at']

def create_dispatch_instruction_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_dispatch_instruction_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_dispatch_instruction_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_dispatch_instruction(record: DispatchInstructionRecord) -> DispatchInstructionRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required dispatch_instruction fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported dispatch_instruction fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required dispatch_instruction fields cannot be empty")
    try:
        if not isinstance(record['destination'], dict) or not {'lat','lon'} <= set(record['destination']): raise ValueError('destination requires latitude and longitude')
        if not -90 <= record['destination']['lat'] <= 90 or not -180 <= record['destination']['lon'] <= 180: raise ValueError('destination coordinates out of range')
        if record['issued_at'] >= record['expires_at']: raise ValueError('dispatch expiry must follow issuance')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed dispatch_instruction domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_dispatch_instruction(record: DispatchInstructionRecord) -> bytes:
    normalized = validate_dispatch_instruction(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_dispatch_instruction(identity: dict, record: DispatchInstructionRecord) -> bytes:
    payload = canonicalize_dispatch_instruction(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_dispatch_instruction(public_key, record: DispatchInstructionRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_dispatch_instruction(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_dispatch_instruction_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_dispatch_instruction_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_dispatch_instruction_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_dispatch_instruction_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class GeoDispatchLedger:
    """SQLite-backed append-only ledger for validated, signed dispatch instructions."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: DispatchInstructionRecord) -> None:
        return
    def publish(self, identity: dict, record: DispatchInstructionRecord) -> bytes:
        normalized = validate_dispatch_instruction(record)
        record_id = str(record['dispatch_id'])
        if record_id is None or not str(record_id).strip():
            raise ValueError("dispatch_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_dispatch_instruction(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate dispatch_instruction identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_geodispatch_workflow(identity: dict, record: DispatchInstructionRecord, ledger: GeoDispatchLedger | None = None) -> dict:
    normalized = validate_dispatch_instruction(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_dispatch_instruction(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> DispatchInstructionRecord:
    return json.loads('{"destination":{"lat":37.7749,"lon":-122.4194},"dispatch_id":"dispatch-1","expires_at":1893463200,"issued_at":1893456000,"vehicle_id":"truck-9"}')
