# Expected behavior

CloudWebhookRegistry: Replace DER public-key export with ML-DSA-65 serialization for webhook registration verifiers. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
