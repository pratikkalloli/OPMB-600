# Migration requirements

CloudWebhookRegistry: Keep signed webhook registration issuance in SQLite and reject duplicate webhook_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
