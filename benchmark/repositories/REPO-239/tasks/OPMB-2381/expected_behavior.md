# Expected behavior

- Preserve the ServiceLevelCredit workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/service_level_credit/workflow.py, src/service_level_credit/crypto.py; the original test is `tests/test_service_level_credit.py::test_task_2381_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_service_level_credit_pqc.py::test_task_2381_identity_separates_signing_and_transport_keys`.
