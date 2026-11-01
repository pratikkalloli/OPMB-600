# Expected behavior

TenantKeyRotation: Replace ECDSA-SHA256 signatures over canonical tenant key rotation claims with ML-DSA-65. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
