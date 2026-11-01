"""NetworkTelemetryCheckpoint: synthetic network telemetry checkpoint workflow."""
from __future__ import annotations
import json, re
from typing import Any

STATES = ['provisioned', 'active', 'rotated', 'retired']
TRANSITIONS = {'provisioned': ['active', 'retired'], 'active': ['rotated', 'retired'], 'rotated': ['active', 'retired'], 'retired': []}
REQUIRED_FIELDS = ['record_id', 'network_element_id', 'evidence_digest', 'event_code', 'sequence', 'state']
RULE_FIELD = 'evidence_digest'
SCOPE_FIELD = 'network_element_id'

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic network telemetry checkpoint record."""
    if not isinstance(record, dict) or set(REQUIRED_FIELDS) - record.keys():
        raise ValueError("record is missing required workflow fields")
    if not isinstance(record.get("record_id"), str) or not record["record_id"].strip():
        raise ValueError("record_id must be a nonempty string")
    if not isinstance(record.get(SCOPE_FIELD), str) or not record[SCOPE_FIELD].strip():
        raise ValueError("workflow scope must be a nonempty string")
    if any(isinstance(record[k], str) and not record[k].strip() for k in REQUIRED_FIELDS if k not in {RULE_FIELD, "state"}):
        raise ValueError("string workflow fields must be nonempty")
    if record["state"] not in STATES:
        raise ValueError("unknown network telemetry checkpoint state")
    value = record[RULE_FIELD]
    if not (isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None):
        raise ValueError("invalid evidence digest")
    return dict(record)

def canonical_record(record: dict[str, Any]) -> bytes:
    """Return deterministic JSON for a validated network telemetry checkpoint."""
    return json.dumps(validate_record(record), sort_keys=True, separators=(",", ":")).encode("utf-8")

def transition_record(record: dict[str, Any], new_state: str) -> dict[str, Any]:
    """Apply the NetworkTelemetryCheckpoint lifecycle without permitting skipped transitions."""
    current = validate_record(record)
    if new_state not in TRANSITIONS[current["state"]]:
        raise ValueError(f"transition {current['state']} -> {new_state} is not permitted")
    current["state"] = new_state
    return validate_record(current)
