# Expected behavior

TenantKeyRotation: Reject malformed public-key encodings when loading tenant key rotation verification keys. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
