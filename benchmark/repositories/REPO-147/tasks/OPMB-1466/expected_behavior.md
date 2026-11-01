# Expected behavior

- Preserve the IdentityAuditBundle workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/identity_audit_bundle/workflow.py, src/identity_audit_bundle/crypto.py; the original test is `tests/test_identity_audit_bundle.py::test_task_1466_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_identity_audit_bundle_pqc.py::test_task_1466_signature_binds_record_context_and_validity`.
