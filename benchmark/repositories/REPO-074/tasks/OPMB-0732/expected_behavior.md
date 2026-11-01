# Expected behavior

- Preserve the DividendDispatch workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/dividend_dispatch/workflow.py, src/dividend_dispatch/crypto.py; the original test is `tests/test_dividend_dispatch.py::test_task_0732_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_dividend_dispatch_pqc.py::test_task_0732_public_key_encoding_round_trips_and_binds_purpose`.
