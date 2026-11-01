# Expected behavior

VectorStoreSnapshot: Keep signed vectorstoresnapshot issuance in SQLite and reject duplicate snapshot_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
