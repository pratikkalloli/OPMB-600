# Expected behavior

- Preserve the VendorBankChange workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/vendor_bank_change/workflow.py, src/vendor_bank_change/crypto.py; the original test is `tests/test_vendor_bank_change.py::test_task_2375_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_vendor_bank_change_pqc.py::test_task_2375_canonical_record_encoding_is_stable`.
