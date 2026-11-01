# Migration requirements

PairingSessionIdentity: Keep signed pairingsessionidentity issuance in SQLite and reject duplicate identity_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
