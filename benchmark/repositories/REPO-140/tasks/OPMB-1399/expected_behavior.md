# Expected behavior

- Preserve the IdentityAttributeCorrection workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/identity_attribute_correction/workflow.py, src/identity_attribute_correction/crypto.py; the original test is `tests/test_identity_attribute_correction.py::test_task_1399_rotation_retires_old_key_version` and PQC migration test is `tests/test_identity_attribute_correction_pqc.py::test_task_1399_rotation_retires_old_key_version`.
