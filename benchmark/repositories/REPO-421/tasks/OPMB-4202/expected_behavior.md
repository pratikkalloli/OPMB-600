# Expected behavior

CloudQuotaGrant: Reject unknown or missing quota grant claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
