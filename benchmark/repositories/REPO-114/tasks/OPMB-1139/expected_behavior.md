# Expected behavior

- Preserve the MaternalScreening workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/maternal_screening/workflow.py, src/maternal_screening/crypto.py; the original test is `tests/test_maternal_screening.py::test_task_1139_rotation_retires_old_key_version` and PQC migration test is `tests/test_maternal_screening_pqc.py::test_task_1139_rotation_retires_old_key_version`.
