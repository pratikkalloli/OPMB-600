# Expected behavior

- Preserve the SalesTaxEvidence workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/sales_tax_evidence/workflow.py, src/sales_tax_evidence/crypto.py; the original test is `tests/test_sales_tax_evidence.py::test_task_2349_rotation_retires_old_key_version` and PQC migration test is `tests/test_sales_tax_evidence_pqc.py::test_task_2349_rotation_retires_old_key_version`.
