# Expected behavior

TenantPolicyBundle: Keep signed tenant policy bundle issuance in SQLite and reject duplicate bundle_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
