# Migration requirements

CloudSchedulerAttestation: Keep signed cloudschedulerattestation issuance in SQLite and reject duplicate attestation_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
