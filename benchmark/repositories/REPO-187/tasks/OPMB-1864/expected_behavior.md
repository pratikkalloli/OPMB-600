# Expected behavior

- Preserve the PermitReceipt workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/permit_receipt/workflow.py, src/permit_receipt/crypto.py; the original test is `tests/test_permit_receipt.py::test_task_1864_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_permit_receipt_pqc.py::test_task_1864_domain_schema_and_policy_reject_invalid_records`.
