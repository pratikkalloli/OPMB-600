# Expected behavior

PipelineConnectorIdentity: Keep signed pipelineconnectoridentity issuance in SQLite and reject duplicate connector_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
