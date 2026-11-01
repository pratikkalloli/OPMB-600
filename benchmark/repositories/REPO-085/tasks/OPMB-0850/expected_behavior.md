# Expected behavior

- Preserve the TradeConfirm workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/trade_confirm/workflow.py, src/trade_confirm/crypto.py; the original test is `tests/test_trade_confirm.py::test_task_0850_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_trade_confirm_pqc.py::test_task_0850_revocation_ledger_persistence_and_cli_workflow`.
