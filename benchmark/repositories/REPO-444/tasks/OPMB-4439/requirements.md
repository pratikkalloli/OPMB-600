# Migration requirements

CloudSessionContinuity: Keep signed cloudsessioncontinuity issuance in SQLite and reject duplicate session_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
