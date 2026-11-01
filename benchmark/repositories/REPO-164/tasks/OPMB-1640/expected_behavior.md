# Expected behavior

- Preserve the StudentMobility workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/student_mobility/workflow.py, src/student_mobility/crypto.py; the original test is `tests/test_student_mobility.py::test_task_1640_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_student_mobility_pqc.py::test_task_1640_revocation_ledger_persistence_and_cli_workflow`.
