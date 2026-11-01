"""ApprovalFlow domain workflows for multi-stage approval signatures and quorum verification."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class ApprovalRequestRecord(TypedDict):
    request_id: str
    stage: int
    approver_id: str
    decision: str
    payload_digest: str

CONTEXT = b"opmb-600:approvalflow:v1"
REQUIRED_FIELDS = ['request_id', 'stage', 'approver_id', 'decision', 'payload_digest']

def create_approval_request_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_approval_request_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_approval_request_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_approval_request(record: ApprovalRequestRecord) -> ApprovalRequestRecord:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required approval_request fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported approval_request fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required approval_request fields cannot be empty")
    try:
        if record['decision'] not in ('approve','reject'): raise ValueError('decision must be approve or reject')
        if not isinstance(record['stage'], int) or record['stage'] < 1: raise ValueError('approval stage must be positive')
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed approval_request domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

    return normalized

def canonicalize_approval_request(record: ApprovalRequestRecord) -> bytes:
    normalized = validate_approval_request(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_approval_request(identity: dict, record: ApprovalRequestRecord) -> bytes:
    payload = canonicalize_approval_request(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_approval_request(public_key, record: ApprovalRequestRecord, envelope: bytes) -> bool:
    try:
        expected = canonicalize_approval_request(record)
    except (ValueError, TypeError, KeyError):
        return False

    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_approval_request_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_approval_request_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_approval_request_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_approval_request_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)


class ApprovalFlowLedger:
    """SQLite-backed append-only ledger for validated, signed approval requests."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: ApprovalRequestRecord) -> None:
        return
    def publish(self, identity: dict, record: ApprovalRequestRecord) -> bytes:
        normalized = validate_approval_request(record)
        record_id = f"{record['request_id']}:{record['stage']}:{record['approver_id']}"
        if record_id is None or not str(record_id).strip():
            raise ValueError("request_id must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_approval_request(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate approval_request identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()
    def approval_quorum_met(self, request_id: str, stage: int, quorum: int, signer_keys: dict[str, object]) -> bool:
        if not isinstance(quorum, int) or quorum < 1:
            raise ValueError("quorum must be positive")
        rows = self._db.execute("SELECT body, signature FROM signed_records").fetchall()
        approvers = set()
        for body, signature in rows:
            item = json.loads(body)
            approver = item["approver_id"]
            if item["request_id"] != request_id or item["stage"] != stage or item["decision"] != "approve":
                continue
            public_key = signer_keys.get(approver)
            if public_key is not None and crypto.verify_document(bytes(signature), public_key, CONTEXT) == bytes(body):
                approvers.add(approver)
        return len(approvers) >= quorum

def run_approvalflow_workflow(identity: dict, record: ApprovalRequestRecord, ledger: ApprovalFlowLedger | None = None) -> dict:
    normalized = validate_approval_request(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_approval_request(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> ApprovalRequestRecord:
    return json.loads('{"approver_id":"alice","decision":"approve","payload_digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","request_id":"change-77","stage":1}')
