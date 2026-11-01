# Expected behavior

- Preserve the ExamAccommodation workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/exam_accommodation/workflow.py, src/exam_accommodation/crypto.py; the original test is `tests/test_exam_accommodation.py::test_task_1650_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_exam_accommodation_pqc.py::test_task_1650_revocation_ledger_persistence_and_cli_workflow`.
