# Migration requirements

FineTuneJobIdentity: Keep signed finetunejobidentity issuance in SQLite and reject duplicate job_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
