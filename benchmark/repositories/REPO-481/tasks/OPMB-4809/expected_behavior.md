# Expected behavior

ModelArtifactSeal: Keep signed modelartifactseal issuance in SQLite and reject duplicate artifact_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
