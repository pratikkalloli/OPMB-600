# Expected behavior

TenantPolicyBundle: Reject unknown or missing tenant policy bundle claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
