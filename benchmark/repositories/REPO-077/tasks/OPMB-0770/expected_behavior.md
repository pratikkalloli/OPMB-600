# Expected behavior

- Preserve the AuditVoucher workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/audit_voucher/workflow.py, src/audit_voucher/crypto.py; the original test is `tests/test_audit_voucher.py::test_task_0770_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_audit_voucher_pqc.py::test_task_0770_revocation_ledger_persistence_and_cli_workflow`.
