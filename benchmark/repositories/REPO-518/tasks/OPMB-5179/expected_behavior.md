# Expected behavior

PhotoUsageClearance: Keep signed photousageclearance issuance in SQLite and reject duplicate clearance_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
