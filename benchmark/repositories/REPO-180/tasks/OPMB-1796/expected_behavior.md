# Expected behavior

- Preserve the AcademicAppeal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/academic_appeal/workflow.py, src/academic_appeal/crypto.py; the original test is `tests/test_academic_appeal.py::test_task_1796_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_academic_appeal_pqc.py::test_task_1796_signature_binds_record_context_and_validity`.
