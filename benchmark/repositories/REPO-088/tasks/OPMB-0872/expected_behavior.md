# Expected behavior

- Preserve the PensionPayout workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/pension_payout/workflow.py, src/pension_payout/crypto.py; the original test is `tests/test_pension_payout.py::test_task_0872_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_pension_payout_pqc.py::test_task_0872_public_key_encoding_round_trips_and_binds_purpose`.
