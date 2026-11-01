# Expected behavior

- Preserve the StudentMobility workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/student_mobility/workflow.py, src/student_mobility/crypto.py; the original test is `tests/test_student_mobility.py::test_task_1633_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_student_mobility_pqc.py::test_task_1633_malformed_serialization_and_wrong_purpose_are_rejected`.
