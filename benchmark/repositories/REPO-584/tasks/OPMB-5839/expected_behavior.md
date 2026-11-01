# Expected behavior

VaultIndexCheckpoint: Keep signed vaultindexcheckpoint issuance in SQLite and reject duplicate checkpoint_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
