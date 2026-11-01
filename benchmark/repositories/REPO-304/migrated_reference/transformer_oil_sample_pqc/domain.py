"""TransformerOilSample: synthetic transformer oil sample workflow."""
from __future__ import annotations
import json, re
from typing import Any

STATES = ['captured', 'checked', 'settled', 'disputed']
TRANSITIONS = {'captured': ['checked', 'disputed'], 'checked': ['settled', 'disputed'], 'settled': [], 'disputed': ['checked']}
REQUIRED_FIELDS = ['record_id', 'asset_id', 'revision_epoch', 'event_code', 'sequence', 'state']
RULE_FIELD = 'revision_epoch'
SCOPE_FIELD = 'asset_id'

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic transformer oil sample record."""
    if not isinstance(record, dict) or set(REQUIRED_FIELDS) - record.keys():
        raise ValueError("record is missing required workflow fields")
    if not isinstance(record.get("record_id"), str) or not record["record_id"].strip():
        raise ValueError("record_id must be a nonempty string")
    if not isinstance(record.get(SCOPE_FIELD), str) or not record[SCOPE_FIELD].strip():
        raise ValueError("workflow scope must be a nonempty string")
    if any(isinstance(record[k], str) and not record[k].strip() for k in REQUIRED_FIELDS if k not in {RULE_FIELD, "state"}):
        raise ValueError("string workflow fields must be nonempty")
    if record["state"] not in STATES:
        raise ValueError("unknown transformer oil sample state")
    value = record[RULE_FIELD]
    if not (type(value) is int and value > 0):
        raise ValueError("invalid revision epoch")
    return dict(record)

def canonical_record(record: dict[str, Any]) -> bytes:
    """Return deterministic JSON for a validated transformer oil sample."""
    return json.dumps(validate_record(record), sort_keys=True, separators=(",", ":")).encode("utf-8")

def transition_record(record: dict[str, Any], new_state: str) -> dict[str, Any]:
    """Apply the TransformerOilSample lifecycle without permitting skipped transitions."""
    current = validate_record(record)
    if new_state not in TRANSITIONS[current["state"]]:
        raise ValueError(f"transition {current['state']} -> {new_state} is not permitted")
    current["state"] = new_state
    return validate_record(current)
