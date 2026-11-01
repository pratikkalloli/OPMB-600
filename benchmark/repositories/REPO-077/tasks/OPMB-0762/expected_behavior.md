# Expected behavior

- Preserve the AuditVoucher workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/audit_voucher/workflow.py, src/audit_voucher/crypto.py; the original test is `tests/test_audit_voucher.py::test_task_0762_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_audit_voucher_pqc.py::test_task_0762_public_key_encoding_round_trips_and_binds_purpose`.
