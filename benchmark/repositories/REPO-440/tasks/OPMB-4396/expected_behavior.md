# Expected behavior

CloudWebhookRegistry: Replace ECDSA-SHA256 signatures over canonical webhook registration claims with ML-DSA-65. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
