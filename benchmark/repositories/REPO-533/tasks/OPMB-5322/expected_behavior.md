# Expected behavior

LiveEventMediaCredential: Reject unknown or missing liveeventmediacredential claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
