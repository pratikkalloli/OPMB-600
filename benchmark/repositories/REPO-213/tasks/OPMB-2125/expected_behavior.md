# Expected behavior

- Preserve the DigitalReceipt workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/digital_receipt/workflow.py, src/digital_receipt/crypto.py; the original test is `tests/test_digital_receipt.py::test_task_2125_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_digital_receipt_pqc.py::test_task_2125_canonical_record_encoding_is_stable`.
