# Expected behavior

PipelineCheckpointSeal: Reject unknown or missing pipelinecheckpointseal claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
