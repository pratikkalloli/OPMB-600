# Expected behavior

StorageScrubResult: Keep signed storagescrubresult issuance in SQLite and reject duplicate result_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
