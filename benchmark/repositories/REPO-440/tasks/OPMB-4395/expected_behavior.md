# Expected behavior

CloudWebhookRegistry: Reject malformed public-key encodings when loading webhook registration verification keys. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
