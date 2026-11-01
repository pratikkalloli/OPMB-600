"""CleanInPlaceRecord: synthetic clean in place record workflow."""
from __future__ import annotations
import json, re
from typing import Any

STATES = ['draft', 'reviewed', 'released', 'retired']
TRANSITIONS = {'draft': ['reviewed', 'retired'], 'reviewed': ['released', 'draft', 'retired'], 'released': ['retired'], 'retired': []}
REQUIRED_FIELDS = ['record_id', 'workcell_id', 'review_class', 'event_code', 'sequence', 'state']
RULE_FIELD = 'review_class'
SCOPE_FIELD = 'workcell_id'

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic clean in place record record."""
    if not isinstance(record, dict) or set(REQUIRED_FIELDS) - record.keys():
        raise ValueError("record is missing required workflow fields")
    if not isinstance(record.get("record_id"), str) or not record["record_id"].strip():
        raise ValueError("record_id must be a nonempty string")
    if not isinstance(record.get(SCOPE_FIELD), str) or not record[SCOPE_FIELD].strip():
        raise ValueError("workflow scope must be a nonempty string")
    if any(isinstance(record[k], str) and not record[k].strip() for k in REQUIRED_FIELDS if k not in {RULE_FIELD, "state"}):
        raise ValueError("string workflow fields must be nonempty")
    if record["state"] not in STATES:
        raise ValueError("unknown clean in place record state")
    value = record[RULE_FIELD]
    if not (value in {'minor', 'major', 'critical'}):
        raise ValueError("invalid review class")
    return dict(record)

def canonical_record(record: dict[str, Any]) -> bytes:
    """Return deterministic JSON for a validated clean in place record."""
    return json.dumps(validate_record(record), sort_keys=True, separators=(",", ":")).encode("utf-8")

def transition_record(record: dict[str, Any], new_state: str) -> dict[str, Any]:
    """Apply the CleanInPlaceRecord lifecycle without permitting skipped transitions."""
    current = validate_record(record)
    if new_state not in TRANSITIONS[current["state"]]:
        raise ValueError(f"transition {current['state']} -> {new_state} is not permitted")
    current["state"] = new_state
    return validate_record(current)
