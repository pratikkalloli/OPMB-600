# Expected behavior

GroupKeyEpochNotice: Keep signed groupkeyepochnotice issuance in SQLite and reject duplicate notice_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
