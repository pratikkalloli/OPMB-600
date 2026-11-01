# Expected behavior

ModelCardApproval: Keep signed modelcardapproval issuance in SQLite and reject duplicate card_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
