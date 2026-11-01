# Expected behavior

StorageScrubResult: Reject unknown or missing storagescrubresult claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
