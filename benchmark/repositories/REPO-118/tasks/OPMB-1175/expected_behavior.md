# Expected behavior

- Preserve the ClinicalAuditBundle workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/clinical_audit_bundle/workflow.py, src/clinical_audit_bundle/crypto.py; the original test is `tests/test_clinical_audit_bundle.py::test_task_1175_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_clinical_audit_bundle_pqc.py::test_task_1175_canonical_record_encoding_is_stable`.
