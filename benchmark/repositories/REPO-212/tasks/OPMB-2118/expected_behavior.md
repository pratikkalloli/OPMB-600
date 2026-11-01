# Expected behavior

- Preserve the SupplierInvoiceMatch workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/supplier_invoice_match/workflow.py, src/supplier_invoice_match/crypto.py; the original test is `tests/test_supplier_invoice_match.py::test_task_2118_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_supplier_invoice_match_pqc.py::test_task_2118_hybrid_envelope_binds_recipient_and_record_context`.
