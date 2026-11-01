"""ToolChangeAuthorization: synthetic tool change workflow."""
from __future__ import annotations
import json, re
from typing import Any

STATES = ['reported', 'authorized', 'changed', 'returned_to_service']
TRANSITIONS = {'reported': ['authorized'], 'authorized': ['changed', 'reported'], 'changed': ['returned_to_service'], 'returned_to_service': ['reported']}
REQUIRED_FIELDS = ['record_id', 'cell_id', 'tool_serial', 'technician_id', 'reason_code', 'state']
RULE_FIELD = 'tool_serial'
SCOPE_FIELD = 'cell_id'

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic tool change record."""
    if not isinstance(record, dict) or set(REQUIRED_FIELDS) - record.keys():
        raise ValueError("record is missing required workflow fields")
    if not isinstance(record.get("record_id"), str) or not record["record_id"].strip():
        raise ValueError("record_id must be a nonempty string")
    if not isinstance(record.get(SCOPE_FIELD), str) or not record[SCOPE_FIELD].strip():
        raise ValueError("workflow scope must be a nonempty string")
    if any(isinstance(record[k], str) and not record[k].strip() for k in REQUIRED_FIELDS if k not in {RULE_FIELD, "state"}):
        raise ValueError("string workflow fields must be nonempty")
    if record["state"] not in STATES:
        raise ValueError("unknown tool change state")
    value = record[RULE_FIELD]
    if not (isinstance(value, str) and re.fullmatch(r'[A-Z0-9]+(?:-[A-Z0-9]+)*', value) is not None and 4 <= len(value) <= 32):
        raise ValueError("invalid tool serial")
    return dict(record)

def canonical_record(record: dict[str, Any]) -> bytes:
    """Return deterministic JSON for a validated tool change."""
    return json.dumps(validate_record(record), sort_keys=True, separators=(",", ":")).encode("utf-8")

def transition_record(record: dict[str, Any], new_state: str) -> dict[str, Any]:
    """Apply the ToolChangeAuthorization lifecycle without permitting skipped transitions."""
    current = validate_record(record)
    if new_state not in TRANSITIONS[current["state"]]:
        raise ValueError(f"transition {current['state']} -> {new_state} is not permitted")
    current["state"] = new_state
    return validate_record(current)
