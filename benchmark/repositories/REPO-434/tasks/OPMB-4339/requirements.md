# Migration requirements

CloudIdentityBridge: Keep signed identity bridge issuance in SQLite and reject duplicate bridge_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
