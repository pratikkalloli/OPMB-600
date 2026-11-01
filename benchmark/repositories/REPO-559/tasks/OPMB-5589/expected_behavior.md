# Expected behavior

PairingSessionIdentity: Keep signed pairingsessionidentity issuance in SQLite and reject duplicate identity_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
