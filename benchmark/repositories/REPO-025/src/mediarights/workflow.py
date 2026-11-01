"""MediaRights domain workflows for protected media distribution and signed rights manifests."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class RightsManifestRecord(TypedDict):
    asset_id: str
    owner: str
    licensee: str
    starts_at: int
    expires_at: int
    rights: list[Any]
    territories: list[Any]

CONTEXT = b"opmb-600:mediarights:v1"
REQUIRED_FIELDS = ['asset_id', 'owner', 'licensee', 'starts_at', 'expires_at', 'rights', 'territories']

def create_rights_manifest_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_rights_manifest_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_rights_manifest_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_rights_manifest(record: RightsManifestRecord) -> RightsManifestRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required rights_manifest fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported rights_manifest fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required rights_manifest fields cannot be empty")
    try:
        if record['starts_at'] >= record['expires_at']: raise ValueError('rights expiry must follow start')
        if not record['rights'] or not record['territories']: raise ValueError('rights and territories must be non-empty')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed rights_manifest domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_rights_manifest(record: RightsManifestRecord) -> bytes:
    normalized = validate_rights_manifest(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_rights_manifest(identity: dict, record: RightsManifestRecord) -> bytes:
    payload = canonicalize_rights_manifest(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_rights_manifest(public_key, record: RightsManifestRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_rights_manifest(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_rights_manifest_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_rights_manifest_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_rights_manifest_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_rights_manifest_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class MediaRightsLedger:
    """SQLite-backed append-only ledger for validated, signed rights manifests."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: RightsManifestRecord) -> None:
        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        for item in rows:
            same_grant = item["asset_id"] == record["asset_id"] and item["licensee"] == record["licensee"]
            overlaps = record["starts_at"] < item["expires_at"] and item["starts_at"] < record["expires_at"]
            if same_grant and overlaps:
                raise ValueError("media-rights grant overlaps an existing active interval")
    def publish(self, identity: dict, record: RightsManifestRecord) -> bytes:
        normalized = validate_rights_manifest(record)
        record_id = f"{record['asset_id']}:{record['licensee']}:{record['starts_at']}"
        if record_id is None or not str(record_id).strip():
            raise ValueError("asset_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_rights_manifest(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate rights_manifest identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_mediarights_workflow(identity: dict, record: RightsManifestRecord, ledger: MediaRightsLedger | None = None) -> dict:
    normalized = validate_rights_manifest(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_rights_manifest(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> RightsManifestRecord:
    return json.loads('{"asset_id":"movie-42","expires_at":1896048000,"licensee":"library-b","owner":"studio-a","rights":["stream"],"starts_at":1893456000,"territories":["US"]}')
