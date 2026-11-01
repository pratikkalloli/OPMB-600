# Expected behavior

- Preserve the ExamAccommodation workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/exam_accommodation/workflow.py, src/exam_accommodation/crypto.py; the original test is `tests/test_exam_accommodation.py::test_task_1642_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_exam_accommodation_pqc.py::test_task_1642_public_key_encoding_round_trips_and_binds_purpose`.
