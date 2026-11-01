# Expected behavior

FeatureFlagRelease: Keep signed featureflagrelease issuance in SQLite and reject duplicate flag_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
