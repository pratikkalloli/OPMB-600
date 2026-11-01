# Expected behavior

TenantKeyRotation: Reject unknown or missing tenant key rotation claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
