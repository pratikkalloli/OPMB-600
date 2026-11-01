# Expected behavior

- Preserve the PurchaseOrderChange workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/purchase_order_change/workflow.py, src/purchase_order_change/crypto.py; the original test is `tests/test_purchase_order_change.py::test_task_2370_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_purchase_order_change_pqc.py::test_task_2370_revocation_ledger_persistence_and_cli_workflow`.
