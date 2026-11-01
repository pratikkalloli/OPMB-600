"""ClinicalConsent domain workflows for synthetic healthcare consent records and revocation."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class ConsentRecordRecord(TypedDict):
    consent_id: str
    subject_token: str
    scopes: list[Any]
    consented_at: int
    expires_at: int

CONTEXT = b"opmb-600:clinicalconsent:v1"
REQUIRED_FIELDS = ['consent_id', 'subject_token', 'scopes', 'consented_at', 'expires_at']

def create_consent_record_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_consent_record_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_consent_record_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_consent_record(record: ConsentRecordRecord) -> ConsentRecordRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required consent_record fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported consent_record fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required consent_record fields cannot be empty")
    try:
        if not record['scopes'] or not all(isinstance(x, str) for x in record['scopes']): raise ValueError('consent scopes must be non-empty strings')
        if record['consented_at'] >= record['expires_at']: raise ValueError('consent expiry must follow consent')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed consent_record domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc
    if not isinstance(normalized["scopes"], list) or not normalized["scopes"] or not all(isinstance(scope, str) and scope.strip() for scope in normalized["scopes"]):
        raise ValueError("consent requires non-empty string scopes")
    return normalized

def canonicalize_consent_record(record: ConsentRecordRecord) -> bytes:
    normalized = validate_consent_record(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_consent_record(identity: dict, record: ConsentRecordRecord) -> bytes:
    payload = canonicalize_consent_record(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_consent_record(public_key, record: ConsentRecordRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_consent_record(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_consent_record_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_consent_record_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_consent_record_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_consent_record_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class ClinicalConsentLedger:
    """SQLite-backed append-only ledger for validated, signed consent records."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: ConsentRecordRecord) -> None:
        return
    def publish(self, identity: dict, record: ConsentRecordRecord) -> bytes:
        normalized = validate_consent_record(record)
        record_id = str(record['consent_id'])
        if record_id is None or not str(record_id).strip():
            raise ValueError("consent_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_consent_record(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate consent_record identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()
    def revoke_consent(self, consent_id: str) -> None:
        exists = self._db.execute("SELECT 1 FROM signed_records WHERE record_id=?", (consent_id,)).fetchone()
        if not exists:
            raise KeyError(consent_id)
        self._db.execute("INSERT OR IGNORE INTO revoked_consents(consent_id) VALUES(?)", (consent_id,))
        self._db.commit()
    def is_consent_active(self, consent_id: str, signing_public, now: int) -> bool:
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (consent_id,)).fetchone()
        if row is None:
            return False
        if self._db.execute("SELECT 1 FROM revoked_consents WHERE consent_id=?", (consent_id,)).fetchone():
            return False
        body, signature = bytes(row[0]), bytes(row[1])
        record = json.loads(body)
        return (crypto.verify_document(signature, signing_public, CONTEXT) == body
                and record["consented_at"] <= now < record["expires_at"])

def run_clinicalconsent_workflow(identity: dict, record: ConsentRecordRecord, ledger: ClinicalConsentLedger | None = None) -> dict:
    normalized = validate_consent_record(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_consent_record(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> ConsentRecordRecord:
    return json.loads('{"consent_id":"consent-1","consented_at":1893456000,"expires_at":1924992000,"scopes":["research:survey"],"subject_token":"subject-opaque-7"}')
