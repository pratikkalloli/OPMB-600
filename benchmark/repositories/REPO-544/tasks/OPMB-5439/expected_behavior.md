# Expected behavior

TeamMessageReceipt: Keep signed teammessagereceipt issuance in SQLite and reject duplicate receipt_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
