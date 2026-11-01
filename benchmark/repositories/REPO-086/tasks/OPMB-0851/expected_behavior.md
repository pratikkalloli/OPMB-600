# Expected behavior

- Preserve the FXQuote workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/f_x_quote/workflow.py, src/f_x_quote/crypto.py; the original test is `tests/test_f_x_quote.py::test_task_0851_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_f_x_quote_pqc.py::test_task_0851_identity_separates_signing_and_transport_keys`.
