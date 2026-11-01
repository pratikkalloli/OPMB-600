# Expected behavior

- Preserve the ResearchDataAccess workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/research_data_access/workflow.py, src/research_data_access/crypto.py; the original test is `tests/test_research_data_access.py::test_task_1560_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_research_data_access_pqc.py::test_task_1560_revocation_ledger_persistence_and_cli_workflow`.
