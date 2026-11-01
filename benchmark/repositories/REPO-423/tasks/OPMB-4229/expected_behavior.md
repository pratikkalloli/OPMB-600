# Expected behavior

BucketManifest: Keep signed bucket manifest issuance in SQLite and reject duplicate manifest_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
