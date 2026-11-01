# Expected behavior

SharedWorkspaceKeyRotation: Reject unknown or missing sharedworkspacekeyrotation claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
