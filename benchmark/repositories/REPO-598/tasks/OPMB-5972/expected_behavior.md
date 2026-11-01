# Expected behavior

BackupCatalogDelta: Reject unknown or missing backupcatalogdelta claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
