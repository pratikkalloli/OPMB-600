# Expected behavior

- Preserve the ExamAccommodation workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/exam_accommodation/workflow.py, src/exam_accommodation/crypto.py; the original test is `tests/test_exam_accommodation.py::test_task_1646_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_exam_accommodation_pqc.py::test_task_1646_signature_binds_record_context_and_validity`.
