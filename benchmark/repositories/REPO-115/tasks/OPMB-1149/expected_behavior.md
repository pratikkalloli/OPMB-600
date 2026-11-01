# Expected behavior

- Preserve the RegistrySubmission workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/registry_submission/workflow.py, src/registry_submission/crypto.py; the original test is `tests/test_registry_submission.py::test_task_1149_rotation_retires_old_key_version` and PQC migration test is `tests/test_registry_submission_pqc.py::test_task_1149_rotation_retires_old_key_version`.
