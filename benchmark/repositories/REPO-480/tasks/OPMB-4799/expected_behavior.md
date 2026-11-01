# Expected behavior

DeploymentDriftRecord: Keep signed deploymentdriftrecord issuance in SQLite and reject duplicate drift_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
