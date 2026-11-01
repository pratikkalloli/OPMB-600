# Expected behavior

TenantKeyRotation: Keep signed tenant key rotation issuance in SQLite and reject duplicate rotation_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
