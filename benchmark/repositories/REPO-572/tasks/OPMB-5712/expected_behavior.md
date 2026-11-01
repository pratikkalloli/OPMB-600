# Expected behavior

RecoveryPointManifest: Reject unknown or missing recoverypointmanifest claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
