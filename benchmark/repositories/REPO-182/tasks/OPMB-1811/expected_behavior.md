# Expected behavior

- Preserve the CivicFilingReceipt workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/civic_filing_receipt/workflow.py, src/civic_filing_receipt/crypto.py; the original test is `tests/test_civic_filing_receipt.py::test_task_1811_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_civic_filing_receipt_pqc.py::test_task_1811_identity_separates_signing_and_transport_keys`.
