# Expected behavior

- Preserve the EscrowRelease workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/escrow_release/workflow.py, src/escrow_release/crypto.py; the original test is `tests/test_escrow_release.py::test_task_0632_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_escrow_release_pqc.py::test_task_0632_public_key_encoding_round_trips_and_binds_purpose`.
