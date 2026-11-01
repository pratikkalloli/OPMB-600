# Expected behavior

- Preserve the ReturnAuthorization workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/return_authorization/workflow.py, src/return_authorization/crypto.py; the original test is `tests/test_return_authorization.py::test_task_2182_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_return_authorization_pqc.py::test_task_2182_public_key_encoding_round_trips_and_binds_purpose`.
