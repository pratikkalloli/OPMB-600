# Expected behavior

MeshServiceLease: Reject unknown or missing service lease claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
