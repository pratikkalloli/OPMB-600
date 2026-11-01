# Expected behavior

ErasureJobApproval: Keep signed erasurejobapproval issuance in SQLite and reject duplicate approval_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
