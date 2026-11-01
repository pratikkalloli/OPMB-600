# Expected behavior

TenantInviteApproval: Keep signed tenant invitation issuance in SQLite and reject duplicate invite_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
