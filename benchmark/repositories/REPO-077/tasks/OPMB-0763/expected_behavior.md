# Expected behavior

- Preserve the AuditVoucher workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/audit_voucher/workflow.py, src/audit_voucher/crypto.py; the original test is `tests/test_audit_voucher.py::test_task_0763_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_audit_voucher_pqc.py::test_task_0763_malformed_serialization_and_wrong_purpose_are_rejected`.
