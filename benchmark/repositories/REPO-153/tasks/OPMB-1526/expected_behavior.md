# Expected behavior

- Preserve the ExamCustody workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/exam_custody/workflow.py, src/exam_custody/crypto.py; the original test is `tests/test_exam_custody.py::test_task_1526_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_exam_custody_pqc.py::test_task_1526_signature_binds_record_context_and_validity`.
