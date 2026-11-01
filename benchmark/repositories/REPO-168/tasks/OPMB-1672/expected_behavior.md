# Expected behavior

- Preserve the ProceedingRelease workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/proceeding_release/workflow.py, src/proceeding_release/crypto.py; the original test is `tests/test_proceeding_release.py::test_task_1672_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_proceeding_release_pqc.py::test_task_1672_public_key_encoding_round_trips_and_binds_purpose`.
