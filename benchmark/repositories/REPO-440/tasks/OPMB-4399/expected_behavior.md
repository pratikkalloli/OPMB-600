# Expected behavior

CloudWebhookRegistry: Keep signed webhook registration issuance in SQLite and reject duplicate webhook_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
