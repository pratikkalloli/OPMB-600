# Expected behavior

- Preserve the SustainabilityClaim workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/sustainability_claim/workflow.py, src/sustainability_claim/crypto.py; the original test is `tests/test_sustainability_claim.py::test_task_2300_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_sustainability_claim_pqc.py::test_task_2300_revocation_ledger_persistence_and_cli_workflow`.
