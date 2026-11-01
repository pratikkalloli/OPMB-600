# Expected behavior

PipelineStepIdentity: Keep signed pipelinestepidentity issuance in SQLite and reject duplicate step_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
