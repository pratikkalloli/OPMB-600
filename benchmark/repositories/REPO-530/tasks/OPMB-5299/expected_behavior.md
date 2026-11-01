# Expected behavior

ArchiveExhibitSeal: Keep signed archiveexhibitseal issuance in SQLite and reject duplicate seal_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
