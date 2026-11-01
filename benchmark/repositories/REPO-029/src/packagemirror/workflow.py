"""PackageMirror domain workflows for software package mirror integrity and signed indexes."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class PackageIndexRecord(TypedDict):
    package: str
    version: str
    platform: str
    digest: str
    published_at: str

CONTEXT = b"opmb-600:packagemirror:v1"
REQUIRED_FIELDS = ['package', 'version', 'platform', 'digest', 'published_at']

def create_package_index_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_package_index_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_package_index_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_package_index(record: PackageIndexRecord) -> PackageIndexRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required package_index fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported package_index fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required package_index fields cannot be empty")
    try:
        if len(str(record['digest'])) != 64: raise ValueError('package digest must be SHA-256 hex')
        if not all(str(record[x]).strip() for x in ('package','version','platform')): raise ValueError('package, version, and platform are required')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed package_index domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_package_index(record: PackageIndexRecord) -> bytes:
    normalized = validate_package_index(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_package_index(identity: dict, record: PackageIndexRecord) -> bytes:
    payload = canonicalize_package_index(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_package_index(public_key, record: PackageIndexRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_package_index(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_package_index_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_package_index_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_package_index_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_package_index_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class PackageMirrorLedger:
    """SQLite-backed append-only ledger for validated, signed package indexes."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: PackageIndexRecord) -> None:
        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        versions = [tuple(int(part) for part in item["version"].split(".")) for item in rows if item["package"] == record["package"] and item["platform"] == record["platform"]]
        incoming = tuple(int(part) for part in record["version"].split("."))
        if versions and incoming <= max(versions):
            raise ValueError("package index version rollback or duplicate")
    def publish(self, identity: dict, record: PackageIndexRecord) -> bytes:
        normalized = validate_package_index(record)
        record_id = f"{record['package']}:{record['platform']}:{record['version']}"
        if record_id is None or not str(record_id).strip():
            raise ValueError("package must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_package_index(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate package_index identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_packagemirror_workflow(identity: dict, record: PackageIndexRecord, ledger: PackageMirrorLedger | None = None) -> dict:
    normalized = validate_package_index(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_package_index(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> PackageIndexRecord:
    return json.loads('{"digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","package":"libsample","platform":"any","published_at":"2030-01-01T00:00:00Z","version":"1.2.3"}')
