# Expected behavior

ServiceAccountRecovery: Reject unknown or missing serviceaccountrecovery claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
