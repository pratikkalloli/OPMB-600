# Expected behavior

- Preserve the CounselAuthorization workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/counsel_authorization/workflow.py, src/counsel_authorization/crypto.py; the original test is `tests/test_counsel_authorization.py::test_task_2091_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_counsel_authorization_pqc.py::test_task_2091_identity_separates_signing_and_transport_keys`.
