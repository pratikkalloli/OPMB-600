# Expected behavior

- Preserve the RevenueShareRecon workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/revenue_share_recon/workflow.py, src/revenue_share_recon/crypto.py; the original test is `tests/test_revenue_share_recon.py::test_task_0650_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_revenue_share_recon_pqc.py::test_task_0650_revocation_ledger_persistence_and_cli_workflow`.
