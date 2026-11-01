# Expected behavior

CloudSessionContinuity: Reject unknown or missing cloudsessioncontinuity claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
