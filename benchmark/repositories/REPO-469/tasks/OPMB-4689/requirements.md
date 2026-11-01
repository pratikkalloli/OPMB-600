# Migration requirements

SecretScanAttestation: Keep signed secretscanattestation issuance in SQLite and reject duplicate scan_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
