# Expected behavior

- Preserve the ScholarshipAward workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/scholarship_award/workflow.py, src/scholarship_award/crypto.py; the original test is `tests/test_scholarship_award.py::test_task_1549_rotation_retires_old_key_version` and PQC migration test is `tests/test_scholarship_award_pqc.py::test_task_1549_rotation_retires_old_key_version`.
