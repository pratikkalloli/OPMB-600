# Migration requirements

SharedFolderAccessGrant: Keep signed sharedfolderaccessgrant issuance in SQLite and reject duplicate grant_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
