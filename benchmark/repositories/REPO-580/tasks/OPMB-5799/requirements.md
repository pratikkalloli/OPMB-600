# Migration requirements

BackupKeyEpochRecord: Keep signed backupkeyepochrecord issuance in SQLite and reject duplicate record_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
