# Expected behavior

APIClientEnrollment: Reject unknown or missing apiclientenrollment claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
