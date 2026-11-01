# Expected behavior

TestResultAttestation: Keep signed testresultattestation issuance in SQLite and reject duplicate attestation_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
