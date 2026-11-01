# Migration requirements

TenantInviteApproval: Keep signed tenant invitation issuance in SQLite and reject duplicate invite_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
