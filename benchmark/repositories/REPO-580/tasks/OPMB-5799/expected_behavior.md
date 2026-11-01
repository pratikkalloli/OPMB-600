# Expected behavior

BackupKeyEpochRecord: Keep signed backupkeyepochrecord issuance in SQLite and reject duplicate record_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
