# Expected behavior

- Preserve the WholesaleQuote workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/wholesale_quote/workflow.py, src/wholesale_quote/crypto.py; the original test is `tests/test_wholesale_quote.py::test_task_2315_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_wholesale_quote_pqc.py::test_task_2315_canonical_record_encoding_is_stable`.
