# Expected behavior

ObjectVersionChain: Keep signed objectversionchain issuance in SQLite and reject duplicate link_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
