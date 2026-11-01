# Expected behavior

- Preserve the IssuanceQuotaGrant workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/issuance_quota_grant/workflow.py, src/issuance_quota_grant/crypto.py; the original test is `tests/test_issuance_quota_grant.py::test_task_1401_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_issuance_quota_grant_pqc.py::test_task_1401_identity_separates_signing_and_transport_keys`.
