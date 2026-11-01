# Expected behavior

NewsCorrectionLedger: Keep signed newscorrectionledger issuance in SQLite and reject duplicate correction_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
