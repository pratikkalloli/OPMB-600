# Expected behavior

- Preserve the RootKeySuccession workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/root_key_succession/workflow.py, src/root_key_succession/crypto.py; the original test is `tests/test_root_key_succession.py::test_task_1479_rotation_retires_old_key_version` and PQC migration test is `tests/test_root_key_succession_pqc.py::test_task_1479_rotation_retires_old_key_version`.
