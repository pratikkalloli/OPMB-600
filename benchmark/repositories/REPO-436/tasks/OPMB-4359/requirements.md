# Migration requirements

SecretsAccessLease: Keep signed secret access lease issuance in SQLite and reject duplicate lease_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
