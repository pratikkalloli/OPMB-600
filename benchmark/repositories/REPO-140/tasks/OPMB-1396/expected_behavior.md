# Expected behavior

- Preserve the IdentityAttributeCorrection workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/identity_attribute_correction/workflow.py, src/identity_attribute_correction/crypto.py; the original test is `tests/test_identity_attribute_correction.py::test_task_1396_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_identity_attribute_correction_pqc.py::test_task_1396_signature_binds_record_context_and_validity`.
