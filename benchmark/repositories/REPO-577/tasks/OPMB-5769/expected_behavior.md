# Expected behavior

ArchiveCatalogSignature: Keep signed archivecatalogsignature issuance in SQLite and reject duplicate signature_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
