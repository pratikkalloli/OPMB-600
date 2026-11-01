# Expected behavior

- Preserve the CivicPetition workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/civic_petition/workflow.py, src/civic_petition/crypto.py; the original test is `tests/test_civic_petition.py::test_task_1940_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_civic_petition_pqc.py::test_task_1940_revocation_ledger_persistence_and_cli_workflow`.
