# Expected behavior

- Preserve the StockTransfer workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/stock_transfer/workflow.py, src/stock_transfer/crypto.py; the original test is `tests/test_stock_transfer.py::test_task_2306_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_stock_transfer_pqc.py::test_task_2306_signature_binds_record_context_and_validity`.
