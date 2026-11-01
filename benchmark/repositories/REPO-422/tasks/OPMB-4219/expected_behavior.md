# Expected behavior

WorkloadPassport: Keep signed workload passport issuance in SQLite and reject duplicate passport_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
