# Expected behavior

BuildArtifactEnvelope: Reject unknown or missing buildartifactenvelope claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
