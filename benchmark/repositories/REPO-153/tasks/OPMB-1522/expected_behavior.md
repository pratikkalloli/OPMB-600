# Expected behavior

- Preserve the ExamCustody workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/exam_custody/workflow.py, src/exam_custody/crypto.py; the original test is `tests/test_exam_custody.py::test_task_1522_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_exam_custody_pqc.py::test_task_1522_public_key_encoding_round_trips_and_binds_purpose`.
