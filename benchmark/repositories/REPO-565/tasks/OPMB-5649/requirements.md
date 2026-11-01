# Migration requirements

OrganizationJoinReceipt: Keep signed organizationjoinreceipt issuance in SQLite and reject duplicate receipt_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
