# Expected behavior

CloudSessionContinuity: Keep signed cloudsessioncontinuity issuance in SQLite and reject duplicate session_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
