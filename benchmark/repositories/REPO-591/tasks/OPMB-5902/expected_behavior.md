# Expected behavior

StorageTenantHandoff: Reject unknown or missing storagetenanthandoff claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
