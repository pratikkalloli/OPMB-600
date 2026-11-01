# Expected behavior

CrossRegionReplicationProof: Keep signed crossregionreplicationproof issuance in SQLite and reject duplicate proof_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
