# Expected behavior

CollaborationRecoveryCode: Keep signed collaborationrecoverycode issuance in SQLite and reject duplicate code_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
