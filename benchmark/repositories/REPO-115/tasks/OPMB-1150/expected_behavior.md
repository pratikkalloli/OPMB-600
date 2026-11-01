# Expected behavior

- Preserve the RegistrySubmission workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/registry_submission/workflow.py, src/registry_submission/crypto.py; the original test is `tests/test_registry_submission.py::test_task_1150_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_registry_submission_pqc.py::test_task_1150_revocation_ledger_persistence_and_cli_workflow`.
