# Expected behavior

CodeOwnerDecisionLog: Keep signed codeownerdecisionlog issuance in SQLite and reject duplicate decision_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
