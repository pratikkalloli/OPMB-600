# Expected behavior

ArchiveFormatMigration: Keep signed archiveformatmigration issuance in SQLite and reject duplicate migration_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
