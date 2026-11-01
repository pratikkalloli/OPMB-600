# Expected behavior

ServiceAccountRecovery: Keep signed serviceaccountrecovery issuance in SQLite and reject duplicate recovery_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
