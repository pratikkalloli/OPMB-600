"""CleanroomProcessTicket: synthetic cleanroom ticket workflow."""
from __future__ import annotations
import json, re
from typing import Any

STATES = ['prepared', 'monitored', 'released', 'quarantined']
TRANSITIONS = {'prepared': ['monitored', 'quarantined'], 'monitored': ['released', 'quarantined'], 'released': ['quarantined'], 'quarantined': ['prepared']}
REQUIRED_FIELDS = ['record_id', 'room_id', 'particle_count', 'sampling_interval', 'operator_id', 'state']
RULE_FIELD = 'particle_count'
SCOPE_FIELD = 'room_id'

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic cleanroom ticket record."""
    if not isinstance(record, dict) or set(REQUIRED_FIELDS) - record.keys():
        raise ValueError("record is missing required workflow fields")
    if not isinstance(record.get("record_id"), str) or not record["record_id"].strip():
        raise ValueError("record_id must be a nonempty string")
    if not isinstance(record.get(SCOPE_FIELD), str) or not record[SCOPE_FIELD].strip():
        raise ValueError("workflow scope must be a nonempty string")
    if any(isinstance(record[k], str) and not record[k].strip() for k in REQUIRED_FIELDS if k not in {RULE_FIELD, "state"}):
        raise ValueError("string workflow fields must be nonempty")
    if record["state"] not in STATES:
        raise ValueError("unknown cleanroom ticket state")
    value = record[RULE_FIELD]
    if not (type(value) is int and 0 <= value <= 1000):
        raise ValueError("invalid particle count")
    return dict(record)

def canonical_record(record: dict[str, Any]) -> bytes:
    """Return deterministic JSON for a validated cleanroom ticket."""
    return json.dumps(validate_record(record), sort_keys=True, separators=(",", ":")).encode("utf-8")

def transition_record(record: dict[str, Any], new_state: str) -> dict[str, Any]:
    """Apply the CleanroomProcessTicket lifecycle without permitting skipped transitions."""
    current = validate_record(record)
    if new_state not in TRANSITIONS[current["state"]]:
        raise ValueError(f"transition {current['state']} -> {new_state} is not permitted")
    current["state"] = new_state
    return validate_record(current)
