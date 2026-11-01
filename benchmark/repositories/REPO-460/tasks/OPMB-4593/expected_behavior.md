# Expected behavior

PipelineStepIdentity: Replace P-256 signer generation for pipelinestepidentity issuers with ML-DSA-65 key generation. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
