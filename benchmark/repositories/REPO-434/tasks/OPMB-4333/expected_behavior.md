# Expected behavior

CloudIdentityBridge: Replace P-256 signer generation for identity bridge issuers with ML-DSA-65 key generation. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
