# Expected behavior

AnimationRenderReceipt: Keep signed animationrenderreceipt issuance in SQLite and reject duplicate receipt_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
