# Expected behavior

FeatureAccessLease: Keep signed featureaccesslease issuance in SQLite and reject duplicate lease_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
