# Expected behavior

- Preserve the CourseCompletion workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/course_completion/workflow.py, src/course_completion/crypto.py; the original test is `tests/test_course_completion.py::test_task_1620_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_course_completion_pqc.py::test_task_1620_revocation_ledger_persistence_and_cli_workflow`.
