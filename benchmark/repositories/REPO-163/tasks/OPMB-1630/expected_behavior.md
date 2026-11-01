# Expected behavior

- Preserve the AcademicLicense workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/academic_license/workflow.py, src/academic_license/crypto.py; the original test is `tests/test_academic_license.py::test_task_1630_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_academic_license_pqc.py::test_task_1630_revocation_ledger_persistence_and_cli_workflow`.
