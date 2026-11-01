# Expected behavior

SharedWorkspaceKeyRotation: Keep signed sharedworkspacekeyrotation issuance in SQLite and reject duplicate rotation_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
