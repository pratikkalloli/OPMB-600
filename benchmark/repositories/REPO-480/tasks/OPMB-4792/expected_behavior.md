# Expected behavior

DeploymentDriftRecord: Reject unknown or missing deploymentdriftrecord claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
