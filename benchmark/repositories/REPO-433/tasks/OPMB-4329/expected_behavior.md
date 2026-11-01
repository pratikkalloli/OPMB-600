# Expected behavior

ObjectRetentionSeal: Keep signed retention seal issuance in SQLite and reject duplicate seal_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
