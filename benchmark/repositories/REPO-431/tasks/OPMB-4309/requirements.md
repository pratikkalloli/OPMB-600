# Migration requirements

TenantPolicyBundle: Keep signed tenant policy bundle issuance in SQLite and reject duplicate bundle_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
