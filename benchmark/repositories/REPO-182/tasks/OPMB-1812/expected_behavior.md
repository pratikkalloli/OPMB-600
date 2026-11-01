# Expected behavior

- Preserve the CivicFilingReceipt workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/civic_filing_receipt/workflow.py, src/civic_filing_receipt/crypto.py; the original test is `tests/test_civic_filing_receipt.py::test_task_1812_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_civic_filing_receipt_pqc.py::test_task_1812_public_key_encoding_round_trips_and_binds_purpose`.
