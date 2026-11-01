# Expected behavior

- Preserve the ExpenseAttest workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/expense_attest/workflow.py, src/expense_attest/crypto.py; the original test is `tests/test_expense_attest.py::test_task_0776_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_expense_attest_pqc.py::test_task_0776_signature_binds_record_context_and_validity`.
