# Expected behavior

TenantKeyRotation: Replace P-256 signer generation for tenant key rotation issuers with ML-DSA-65 key generation. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
