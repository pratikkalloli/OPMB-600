# Expected behavior

- Preserve the AuditVoucher workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/audit_voucher/workflow.py, src/audit_voucher/crypto.py; the original test is `tests/test_audit_voucher.py::test_task_0765_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_audit_voucher_pqc.py::test_task_0765_canonical_record_encoding_is_stable`.
