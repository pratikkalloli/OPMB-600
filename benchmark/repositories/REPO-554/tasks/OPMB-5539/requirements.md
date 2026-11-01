# Migration requirements

RemoteWorkshopCredential: Keep signed remoteworkshopcredential issuance in SQLite and reject duplicate credential_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
