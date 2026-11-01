# Migration requirements

PipelineStepIdentity: Keep signed pipelinestepidentity issuance in SQLite and reject duplicate step_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
