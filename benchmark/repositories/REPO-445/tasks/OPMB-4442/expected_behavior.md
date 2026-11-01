# Expected behavior

ManagedDatabaseGrant: Reject unknown or missing manageddatabasegrant claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
