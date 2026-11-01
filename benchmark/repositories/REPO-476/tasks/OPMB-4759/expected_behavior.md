# Expected behavior

VulnerabilityWaiverSeal: Keep signed vulnerabilitywaiverseal issuance in SQLite and reject duplicate waiver_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
