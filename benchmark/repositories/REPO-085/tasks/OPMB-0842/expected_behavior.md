# Expected behavior

- Preserve the TradeConfirm workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/trade_confirm/workflow.py, src/trade_confirm/crypto.py; the original test is `tests/test_trade_confirm.py::test_task_0842_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_trade_confirm_pqc.py::test_task_0842_public_key_encoding_round_trips_and_binds_purpose`.
