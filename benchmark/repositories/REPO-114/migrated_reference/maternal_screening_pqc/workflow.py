"""Domain rules for MaternalScreening's An authorized maternal screening result release operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow."""
from __future__ import annotations
import json, re, sqlite3, time
from pathlib import Path
from . import crypto

CONTEXT = b"opmb-scale600:maternal_screening:v1"
DOMAIN = "healthcare_life_sciences"
DOMAIN_FIELDS = ['patient_ref', 'provider_ref', 'purpose_code', 'source_ref', 'sequence']
REQUIRED_FIELDS = ["record_id", "subject_ref", "workflow_ref", "issued_at", "expires_at", *DOMAIN_FIELDS]
POLICY_VARIANT = 5
POLICY_FIELD = "sequence"

def create_maternal_screening_identity():
    signing_private, signing_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": signing_private, "signing_public": signing_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_maternal_screening_public_key(public_key, purpose: str) -> bytes:
    return crypto.serialize_public_key(public_key, purpose)

def load_maternal_screening_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_maternal_screening_record(record: dict) -> dict:
    if not isinstance(record, dict) or set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record fields do not match the MaternalScreening schema")
    if any(value is None or value == "" for value in record.values()):
        raise ValueError("record values must be present")
    if not isinstance(record["issued_at"], int) or not isinstance(record["expires_at"], int) or record["issued_at"] >= record["expires_at"]:
        raise ValueError("record validity interval is invalid")
    if any(not isinstance(record[key], str) or not record[key].strip() for key in ("record_id", "subject_ref", "workflow_ref")):
        raise ValueError("record identifiers must be non-empty text")
    if DOMAIN == "financial_services_insurance":
        if not isinstance(record["amount_minor"], int) or record["amount_minor"] <= POLICY_VARIANT * 100:
            raise ValueError("amount violates the transaction floor")
        if not re.fullmatch(r"[A-Z]{3}", record["currency"]): raise ValueError("currency must be ISO-style uppercase text")
    elif DOMAIN == "healthcare_life_sciences":
        if not isinstance(record["sequence"], int) or record["sequence"] <= POLICY_VARIANT:
            raise ValueError("clinical record sequence must advance")
        if not record["purpose_code"].startswith("care:"): raise ValueError("clinical purpose must be scoped")
    elif DOMAIN == "identity_credentials_pki_trust":
        if not isinstance(record["assurance_level"], int) or not POLICY_VARIANT + 1 <= record["assurance_level"] <= 4:
            raise ValueError("credential assurance level is outside issuer policy")
        if len(record["credential_type"]) > 64: raise ValueError("credential type is too long")
    elif DOMAIN == "education_research":
        if not re.fullmatch(r"20[0-9]{2}-20[0-9]{2}", record["academic_period"]):
            raise ValueError("academic period must use YYYY-YYYY form")
        if not isinstance(record["sequence"], int) or record["sequence"] < 1: raise ValueError("academic sequence must be positive")
    elif DOMAIN == "legal_civic_public_records":
        allowed_states = ["filed", "served", "recorded", "reviewed", "published", "closed"]
        if not isinstance(record["filing_sequence"], int) or record["filing_sequence"] <= POLICY_VARIANT:
            raise ValueError("filing sequence violates authority policy")
        if record["custody_state"] not in allowed_states: raise ValueError("invalid public-record custody state")
    elif DOMAIN == "commerce_business_transactions":
        if not isinstance(record["quantity"], int) or record["quantity"] < POLICY_VARIANT + 1:
            raise ValueError("transaction quantity violates merchant policy")
        if len(record["region"]) != 2 or not record["region"].isalpha(): raise ValueError("region must be a two-letter code")
    try:
        return json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

def canonicalize_maternal_screening_record(record: dict) -> bytes:
    return json.dumps(validate_maternal_screening_record(record), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_maternal_screening_record(identity: dict, record: dict) -> bytes:
    return crypto.sign_document(canonicalize_maternal_screening_record(record), identity["signing_private"], CONTEXT)

def verify_maternal_screening_record(public_key, record: dict, envelope: bytes, now: int | None = None) -> bool:
    try: canonical = canonicalize_maternal_screening_record(record)
    except (ValueError, TypeError, KeyError): return False
    now = int(time.time()) if now is None else now
    if not isinstance(now, int) or not record["issued_at"] <= now < record["expires_at"]: return False
    return crypto.verify_document(envelope, public_key, CONTEXT) == canonical

def seal_maternal_screening_payload(public_key, plaintext: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip(): raise ValueError("record id is required for envelope binding")
    return crypto.seal_payload(plaintext, public_key, CONTEXT + b":" + record_id.encode())

def open_maternal_screening_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip(): raise ValueError("record id is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_maternal_screening_identity(registry: crypto.KeyRegistry, identity_id: str): return registry.rotate(identity_id)
def revoke_maternal_screening_identity(registry: crypto.KeyRegistry, identity_id: str): return registry.revoke(identity_id)

class MaternalScreeningLedger:
    """Persistent append-only store enforcing duplicate and domain record policy."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records(record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.commit()
    def publish(self, identity: dict, record: dict) -> bytes:
        canonical = canonicalize_maternal_screening_record(record)
        signature = crypto.sign_document(canonical, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (record["record_id"], canonical, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc: raise ValueError("duplicate domain record id") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None: raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self): self._db.close()

def run_maternal_screening_workflow(identity: dict, record: dict, ledger: MaternalScreeningLedger | None = None) -> dict:
    normalized = validate_maternal_screening_record(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_maternal_screening_record(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> dict:
    return {'record_id': 'sample-001', 'subject_ref': 'subject-17', 'workflow_ref': 'maternal_screening-workflow', 'issued_at': 1800000000, 'expires_at': 1900000000, 'patient_ref': 'patient-sim-2', 'provider_ref': 'provider-4', 'purpose_code': 'care:workflow', 'source_ref': 'source-3', 'sequence': 6}
