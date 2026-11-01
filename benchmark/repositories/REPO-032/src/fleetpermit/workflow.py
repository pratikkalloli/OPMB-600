"""FleetPermit domain workflows for vehicle permit issuance and offline verification simulation."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class VehiclePermitRecord(TypedDict):
    permit_id: str
    vehicle_id: str
    jurisdiction: str
    permit_class: str
    valid_from: int
    valid_until: int

CONTEXT = b"opmb-600:fleetpermit:v1"
REQUIRED_FIELDS = ['permit_id', 'vehicle_id', 'jurisdiction', 'permit_class', 'valid_from', 'valid_until']

def create_vehicle_permit_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_vehicle_permit_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_vehicle_permit_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_vehicle_permit(record: VehiclePermitRecord) -> VehiclePermitRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required vehicle_permit fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported vehicle_permit fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required vehicle_permit fields cannot be empty")
    try:
        if record['valid_from'] >= record['valid_until']: raise ValueError('permit validity interval is invalid')
        if not all(str(record[x]).strip() for x in ('vehicle_id','jurisdiction','permit_class')): raise ValueError('permit identity fields are required')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed vehicle_permit domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_vehicle_permit(record: VehiclePermitRecord) -> bytes:
    normalized = validate_vehicle_permit(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_vehicle_permit(identity: dict, record: VehiclePermitRecord) -> bytes:
    payload = canonicalize_vehicle_permit(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_vehicle_permit(public_key, record: VehiclePermitRecord, envelope: bytes, now: int | None = None) -> bool:
    try:
        expected = canonicalize_vehicle_permit(record)
    except (ValueError, TypeError, KeyError):
        return False
    if now is None:
        now = int(__import__("time").time())
    if not isinstance(now, int) or not record.get("valid_from") <= now < record.get("valid_until"):
        return False
    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_vehicle_permit_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_vehicle_permit_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_vehicle_permit_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_vehicle_permit_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class FleetPermitLedger:
    """SQLite-backed append-only ledger for validated, signed vehicle permits."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: VehiclePermitRecord) -> None:
        return
    def publish(self, identity: dict, record: VehiclePermitRecord) -> bytes:
        normalized = validate_vehicle_permit(record)
        record_id = str(record['permit_id'])
        if record_id is None or not str(record_id).strip():
            raise ValueError("permit_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_vehicle_permit(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate vehicle_permit identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_fleetpermit_workflow(identity: dict, record: VehiclePermitRecord, ledger: FleetPermitLedger | None = None) -> dict:
    normalized = validate_vehicle_permit(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_vehicle_permit(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> VehiclePermitRecord:
    return json.loads('{"jurisdiction":"CA","permit_class":"oversize","permit_id":"permit-001","valid_from":1893456000,"valid_until":1924992000,"vehicle_id":"truck-7"}')
