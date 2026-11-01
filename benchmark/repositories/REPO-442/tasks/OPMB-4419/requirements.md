# Migration requirements

APIClientEnrollment: Keep signed apiclientenrollment issuance in SQLite and reject duplicate client_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
