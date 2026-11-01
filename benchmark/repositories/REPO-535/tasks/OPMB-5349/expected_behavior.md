# Expected behavior

AdInsertionAuthorization: Keep signed adinsertionauthorization issuance in SQLite and reject duplicate authorization_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
