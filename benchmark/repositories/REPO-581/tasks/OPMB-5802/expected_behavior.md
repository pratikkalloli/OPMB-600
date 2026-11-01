# Expected behavior

ImmutableRetentionLease: Reject unknown or missing immutableretentionlease claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
