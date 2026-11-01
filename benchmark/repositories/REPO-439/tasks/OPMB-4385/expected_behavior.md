# Expected behavior

TenantInviteApproval: Reject malformed public-key encodings when loading tenant invitation verification keys. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
