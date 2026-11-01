# Expected behavior

AvailabilityBlockSeal: Keep signed availabilityblockseal issuance in SQLite and reject duplicate block_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
