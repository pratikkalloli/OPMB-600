# Expected behavior

SecretScanAttestation: Reject unknown or missing secretscanattestation claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
