# Expected behavior

- Preserve the RegistrySubmission workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/registry_submission/workflow.py, src/registry_submission/crypto.py; the original test is `tests/test_registry_submission.py::test_task_1142_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_registry_submission_pqc.py::test_task_1142_public_key_encoding_round_trips_and_binds_purpose`.
