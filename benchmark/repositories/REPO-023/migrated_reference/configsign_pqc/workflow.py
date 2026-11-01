"""ConfigSign domain workflows for signed configuration distribution and rollback protection."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class ConfigurationReleaseRecord(TypedDict):
    system_id: str
    version: int
    settings: dict[str, Any]
    issued_at: str

CONTEXT = b"opmb-600:configsign:v1"
REQUIRED_FIELDS = ['system_id', 'version', 'settings', 'issued_at']

def create_configuration_release_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_configuration_release_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_configuration_release_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_configuration_release(record: ConfigurationReleaseRecord) -> ConfigurationReleaseRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required configuration_release fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported configuration_release fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required configuration_release fields cannot be empty")
    try:
        if not isinstance(record['version'], int) or record['version'] < 1: raise ValueError('configuration version must be positive')
        if not isinstance(record['settings'], dict): raise ValueError('settings must be an object')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed configuration_release domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_configuration_release(record: ConfigurationReleaseRecord) -> bytes:
    normalized = validate_configuration_release(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_configuration_release(identity: dict, record: ConfigurationReleaseRecord) -> bytes:
    payload = canonicalize_configuration_release(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_configuration_release(public_key, record: ConfigurationReleaseRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_configuration_release(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_configuration_release_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_configuration_release_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_configuration_release_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_configuration_release_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class ConfigSignLedger:
    """SQLite-backed append-only ledger for validated, signed configuration releases."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: ConfigurationReleaseRecord) -> None:
        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        versions = [item["version"] for item in rows if item["system_id"] == record["system_id"]]
        if versions and record["version"] <= max(versions):
            raise ValueError("configuration version rollback or duplicate")
    def publish(self, identity: dict, record: ConfigurationReleaseRecord) -> bytes:
        normalized = validate_configuration_release(record)
        record_id = f"{record['system_id']}:{record['version']}"
        if record_id is None or not str(record_id).strip():
            raise ValueError("system_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_configuration_release(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate configuration_release identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_configsign_workflow(identity: dict, record: ConfigurationReleaseRecord, ledger: ConfigSignLedger | None = None) -> dict:
    normalized = validate_configuration_release(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_configuration_release(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> ConfigurationReleaseRecord:
    return json.loads('{"issued_at":"2030-01-01T00:00:00Z","settings":{"feature_x":true,"log_level":"info"},"system_id":"edge-west","version":1}')
