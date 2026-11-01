# Expected behavior

- Preserve the FinanceConsent workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/finance_consent/workflow.py, src/finance_consent/crypto.py; the original test is `tests/test_finance_consent.py::test_task_0889_rotation_retires_old_key_version` and PQC migration test is `tests/test_finance_consent_pqc.py::test_task_0889_rotation_retires_old_key_version`.
