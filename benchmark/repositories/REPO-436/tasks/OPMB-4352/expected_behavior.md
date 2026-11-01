# Expected behavior

SecretsAccessLease: Reject unknown or missing secret access lease claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
