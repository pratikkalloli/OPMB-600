# Expected behavior

- Preserve the SelectiveDisclosure workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/selective_disclosure/workflow.py, src/selective_disclosure/crypto.py; the original test is `tests/test_selective_disclosure.py::test_task_1449_rotation_retires_old_key_version` and PQC migration test is `tests/test_selective_disclosure_pqc.py::test_task_1449_rotation_retires_old_key_version`.
