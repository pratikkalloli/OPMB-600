"""LineClearanceToken: synthetic line clearance workflow."""
from __future__ import annotations
import json, re
from typing import Any

STATES = ['requested', 'inspected', 'cleared', 'revoked']
TRANSITIONS = {'requested': ['inspected', 'revoked'], 'inspected': ['cleared', 'requested', 'revoked'], 'cleared': ['revoked'], 'revoked': []}
REQUIRED_FIELDS = ['record_id', 'line_id', 'product_code', 'clearance_code', 'shift_id', 'state']
RULE_FIELD = 'clearance_code'
SCOPE_FIELD = 'line_id'

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic line clearance record."""
    if not isinstance(record, dict) or set(REQUIRED_FIELDS) - record.keys():
        raise ValueError("record is missing required workflow fields")
    if not isinstance(record.get("record_id"), str) or not record["record_id"].strip():
        raise ValueError("record_id must be a nonempty string")
    if not isinstance(record.get(SCOPE_FIELD), str) or not record[SCOPE_FIELD].strip():
        raise ValueError("workflow scope must be a nonempty string")
    if any(isinstance(record[k], str) and not record[k].strip() for k in REQUIRED_FIELDS if k not in {RULE_FIELD, "state"}):
        raise ValueError("string workflow fields must be nonempty")
    if record["state"] not in STATES:
        raise ValueError("unknown line clearance state")
    value = record[RULE_FIELD]
    if not (isinstance(value, str) and re.fullmatch(r'[A-Z0-9]+(?:-[A-Z0-9]+)*', value) is not None and 4 <= len(value) <= 32):
        raise ValueError("invalid clearance code")
    return dict(record)

def canonical_record(record: dict[str, Any]) -> bytes:
    """Return deterministic JSON for a validated line clearance."""
    return json.dumps(validate_record(record), sort_keys=True, separators=(",", ":")).encode("utf-8")

def transition_record(record: dict[str, Any], new_state: str) -> dict[str, Any]:
    """Apply the LineClearanceToken lifecycle without permitting skipped transitions."""
    current = validate_record(record)
    if new_state not in TRANSITIONS[current["state"]]:
        raise ValueError(f"transition {current['state']} -> {new_state} is not permitted")
    current["state"] = new_state
    return validate_record(current)
