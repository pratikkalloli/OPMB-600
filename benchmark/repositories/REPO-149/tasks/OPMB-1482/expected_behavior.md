# Expected behavior

- Preserve the DirectorySyncProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/directory_sync_proof/workflow.py, src/directory_sync_proof/crypto.py; the original test is `tests/test_directory_sync_proof.py::test_task_1482_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_directory_sync_proof_pqc.py::test_task_1482_public_key_encoding_round_trips_and_binds_purpose`.
