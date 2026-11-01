# Expected behavior

- Preserve the RecoveryShare workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/recovery_share/workflow.py, src/recovery_share/crypto.py; the original test is `tests/test_recovery_share.py::test_task_1292_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_recovery_share_pqc.py::test_task_1292_public_key_encoding_round_trips_and_binds_purpose`.
