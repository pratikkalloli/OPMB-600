# Migration requirements

PipelineConnectorIdentity: Keep signed pipelineconnectoridentity issuance in SQLite and reject duplicate connector_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
