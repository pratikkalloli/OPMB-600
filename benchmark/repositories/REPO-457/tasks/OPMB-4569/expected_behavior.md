# Expected behavior

DeploymentPlanApproval: Keep signed deploymentplanapproval issuance in SQLite and reject duplicate plan_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
