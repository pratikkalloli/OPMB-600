# Expected behavior

- Preserve the WarrantyClaim workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/warranty_claim/workflow.py, src/warranty_claim/crypto.py; the original test is `tests/test_warranty_claim.py::test_task_2140_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_warranty_claim_pqc.py::test_task_2140_revocation_ledger_persistence_and_cli_workflow`.
