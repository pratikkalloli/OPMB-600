# Expected behavior

- Preserve the FinanceConsent workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/finance_consent/workflow.py, src/finance_consent/crypto.py; the original test is `tests/test_finance_consent.py::test_task_0882_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_finance_consent_pqc.py::test_task_0882_public_key_encoding_round_trips_and_binds_purpose`.
