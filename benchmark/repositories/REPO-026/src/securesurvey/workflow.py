"""SecureSurvey domain workflows for encrypted survey responses and signed submission receipts."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class SurveySubmissionRecord(TypedDict):
    survey_id: str
    response_id: str
    answers: dict[str, Any]
    submitted_at: str

CONTEXT = b"opmb-600:securesurvey:v1"
REQUIRED_FIELDS = ['survey_id', 'response_id', 'answers', 'submitted_at']

def create_survey_submission_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_survey_submission_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_survey_submission_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_survey_submission(record: SurveySubmissionRecord) -> SurveySubmissionRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required survey_submission fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported survey_submission fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required survey_submission fields cannot be empty")
    try:
        if not isinstance(record['answers'], dict) or not record['answers']: raise ValueError('answers must be a non-empty object')
        if not str(record['survey_id']).strip(): raise ValueError('survey id is required')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed survey_submission domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_survey_submission(record: SurveySubmissionRecord) -> bytes:
    normalized = validate_survey_submission(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_survey_submission(identity: dict, record: SurveySubmissionRecord) -> bytes:
    payload = canonicalize_survey_submission(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_survey_submission(public_key, record: SurveySubmissionRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_survey_submission(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_survey_submission_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_survey_submission_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_survey_submission_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_survey_submission_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class SecureSurveyLedger:
    """SQLite-backed append-only ledger for validated, signed survey submissions."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: SurveySubmissionRecord) -> None:
        return
    def publish(self, identity: dict, record: SurveySubmissionRecord) -> bytes:
        normalized = validate_survey_submission(record)
        record_id = str(record['response_id'])
        if record_id is None or not str(record_id).strip():
            raise ValueError("response_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_survey_submission(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate survey_submission identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()


def run_securesurvey_workflow(identity: dict, record: SurveySubmissionRecord, ledger: SecureSurveyLedger | None = None) -> dict:
    normalized = validate_survey_submission(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_survey_submission(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> SurveySubmissionRecord:
    return json.loads('{"answers":{"q1":"yes","q2":4},"response_id":"resp-001","submitted_at":"2030-01-01T00:00:00Z","survey_id":"study-1"}')
