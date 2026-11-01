# Migration requirements

SharedWorkspaceKeyRotation: Keep signed sharedworkspacekeyrotation issuance in SQLite and reject duplicate rotation_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
