"""DesktopUpdateProof domain workflows for desktop software update integrity and signed releases."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class UpdateReleaseRecord(TypedDict):
    product: str
    version: str
    platform: str
    sha256: str
    released_at: str

CONTEXT = b"opmb-600:desktopupdateproof:v1"
REQUIRED_FIELDS = ['product', 'version', 'platform', 'sha256', 'released_at']

def create_update_release_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_update_release_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_update_release_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_update_release(record: UpdateReleaseRecord) -> UpdateReleaseRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required update_release fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported update_release fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required update_release fields cannot be empty")
    try:
        if len(str(record['sha256'])) != 64: raise ValueError('release digest must be SHA-256 hex')
        if not all(str(record[x]).strip() for x in ('product','version','platform')): raise ValueError('product, version, and platform are required')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed update_release domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_update_release(record: UpdateReleaseRecord) -> bytes:
    normalized = validate_update_release(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_update_release(identity: dict, record: UpdateReleaseRecord) -> bytes:
    payload = canonicalize_update_release(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_update_release(public_key, record: UpdateReleaseRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_update_release(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_update_release_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_update_release_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_update_release_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_update_release_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class DesktopUpdateProofLedger:
    """SQLite-backed append-only ledger for validated, signed desktop update releases."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: UpdateReleaseRecord) -> None:
        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        versions = [tuple(int(part) for part in item["version"].split(".")) for item in rows if item["product"] == record["product"] and item["platform"] == record["platform"]]
        incoming = tuple(int(part) for part in record["version"].split("."))
        if versions and incoming <= max(versions):
            raise ValueError("desktop update version rollback or duplicate")
    def publish(self, identity: dict, record: UpdateReleaseRecord) -> bytes:
        normalized = validate_update_release(record)
        record_id = f"{record['product']}:{record['platform']}:{record['version']}"
        if record_id is None or not str(record_id).strip():
            raise ValueError("product must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_update_release(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate update_release identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_desktopupdateproof_workflow(identity: dict, record: UpdateReleaseRecord, ledger: DesktopUpdateProofLedger | None = None) -> dict:
    normalized = validate_update_release(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_update_release(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> UpdateReleaseRecord:
    return json.loads('{"platform":"windows-x64","product":"editor","released_at":"2030-01-01T00:00:00Z","sha256":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","version":"2.4.0"}')
