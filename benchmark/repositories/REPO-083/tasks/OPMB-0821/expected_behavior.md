# Expected behavior

- Preserve the ChargebackFile workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/chargeback_file/workflow.py, src/chargeback_file/crypto.py; the original test is `tests/test_chargeback_file.py::test_task_0821_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_chargeback_file_pqc.py::test_task_0821_identity_separates_signing_and_transport_keys`.
