# Migration requirements

ReplicaRepairAuthorization: Keep signed replicarepairauthorization issuance in SQLite and reject duplicate authorization_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
