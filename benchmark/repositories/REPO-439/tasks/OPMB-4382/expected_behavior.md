# Expected behavior

TenantInviteApproval: Reject unknown or missing tenant invitation claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
