# Expected behavior

BackupCatalogDelta: Keep signed backupcatalogdelta issuance in SQLite and reject duplicate delta_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
