# Expected behavior

- Preserve the PensionPayout workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/pension_payout/workflow.py, src/pension_payout/crypto.py; the original test is `tests/test_pension_payout.py::test_task_0871_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_pension_payout_pqc.py::test_task_0871_identity_separates_signing_and_transport_keys`.
