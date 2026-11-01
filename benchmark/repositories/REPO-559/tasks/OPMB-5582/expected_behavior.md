# Expected behavior

PairingSessionIdentity: Reject unknown or missing pairingsessionidentity claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
