# Expected behavior

WorkspaceMemberGrant: Keep signed workspacemembergrant issuance in SQLite and reject duplicate grant_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
