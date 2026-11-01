# Expected behavior

- Preserve the BiobankCustody workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/biobank_custody/workflow.py, src/biobank_custody/crypto.py; the original test is `tests/test_biobank_custody.py::test_task_0980_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_biobank_custody_pqc.py::test_task_0980_revocation_ledger_persistence_and_cli_workflow`.
