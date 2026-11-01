# Expected behavior

BuildCacheIntegrity: Keep signed buildcacheintegrity issuance in SQLite and reject duplicate cache_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
