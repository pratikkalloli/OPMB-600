# Expected behavior

- Preserve the SurgicalChecklist workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/surgical_checklist/workflow.py, src/surgical_checklist/crypto.py; the original test is `tests/test_surgical_checklist.py::test_task_1119_rotation_retires_old_key_version` and PQC migration test is `tests/test_surgical_checklist_pqc.py::test_task_1119_rotation_retires_old_key_version`.
