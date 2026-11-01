"""MailGuard domain workflows for secure email envelopes and attachments."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class MailEnvelopeRecord(TypedDict):
    message_id: str
    sender: str
    recipient: str
    subject: str
    body: str
    attachments: list[Any]

CONTEXT = b"opmb-600:mailguard:v1"
REQUIRED_FIELDS = ['message_id', 'sender', 'recipient', 'subject', 'body', 'attachments']

def create_mail_envelope_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_mail_envelope_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_mail_envelope_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_mail_envelope(record: MailEnvelopeRecord) -> MailEnvelopeRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required mail_envelope fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported mail_envelope fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required mail_envelope fields cannot be empty")
    try:
        if '@' not in str(record['sender']) or '@' not in str(record['recipient']): raise ValueError('sender and recipient must be email addresses')
        if not isinstance(record['attachments'], list): raise ValueError('attachments must be a list')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed mail_envelope domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc
    names = [item.get("name") for item in normalized["attachments"] if isinstance(item, dict)]
    if len(names) != len(normalized["attachments"]) or len(names) != len(set(names)):
        raise ValueError("attachments must be objects with distinct names")
    return normalized

def canonicalize_mail_envelope(record: MailEnvelopeRecord) -> bytes:
    normalized = validate_mail_envelope(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_mail_envelope(identity: dict, record: MailEnvelopeRecord) -> bytes:
    payload = canonicalize_mail_envelope(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_mail_envelope(public_key, record: MailEnvelopeRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_mail_envelope(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_mail_envelope_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_mail_envelope_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_mail_envelope_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_mail_envelope_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class MailGuardLedger:
    """SQLite-backed append-only ledger for validated, signed mail envelopes."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: MailEnvelopeRecord) -> None:
        return
    def publish(self, identity: dict, record: MailEnvelopeRecord) -> bytes:
        normalized = validate_mail_envelope(record)
        record_id = str(record['message_id'])
        if record_id is None or not str(record_id).strip():
            raise ValueError("message_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_mail_envelope(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate mail_envelope identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_mailguard_workflow(identity: dict, record: MailEnvelopeRecord, ledger: MailGuardLedger | None = None) -> dict:
    normalized = validate_mail_envelope(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_mail_envelope(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> MailEnvelopeRecord:
    return json.loads('{"attachments":[{"digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","name":"report.pdf"}],"body":"Quarterly report attached","message_id":"mail-001","recipient":"recipient@example.test","sender":"sender@example.test","subject":"Report"}')
