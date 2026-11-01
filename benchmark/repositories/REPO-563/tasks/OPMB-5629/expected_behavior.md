# Expected behavior

ReviewRoundCompletion: Keep signed reviewroundcompletion issuance in SQLite and reject duplicate completion_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
