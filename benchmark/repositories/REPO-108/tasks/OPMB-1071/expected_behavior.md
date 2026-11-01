# Expected behavior

- Preserve the TelehealthReceipt workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/telehealth_receipt/workflow.py, src/telehealth_receipt/crypto.py; the original test is `tests/test_telehealth_receipt.py::test_task_1071_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_telehealth_receipt_pqc.py::test_task_1071_identity_separates_signing_and_transport_keys`.
