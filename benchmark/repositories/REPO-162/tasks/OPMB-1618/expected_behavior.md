# Expected behavior

- Preserve the CourseCompletion workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/course_completion/workflow.py, src/course_completion/crypto.py; the original test is `tests/test_course_completion.py::test_task_1618_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_course_completion_pqc.py::test_task_1618_hybrid_envelope_binds_recipient_and_record_context`.
