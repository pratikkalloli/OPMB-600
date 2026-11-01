# Expected behavior

FeatureStoreMutationLog: Keep signed featurestoremutationlog issuance in SQLite and reject duplicate event_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
