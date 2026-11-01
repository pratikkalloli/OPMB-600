# Expected behavior

RegionalFailoverProof: Keep signed regional failover proof issuance in SQLite and reject duplicate failover_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
