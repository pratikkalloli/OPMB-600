# Expected behavior

- Preserve the DirectDebit workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/direct_debit/workflow.py, src/direct_debit/crypto.py; the original test is `tests/test_direct_debit.py::test_task_0801_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_direct_debit_pqc.py::test_task_0801_identity_separates_signing_and_transport_keys`.
