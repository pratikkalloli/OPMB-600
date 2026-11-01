# Expected behavior

- Preserve the CredentialPresentation workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/credential_presentation/workflow.py, src/credential_presentation/crypto.py; the original test is `tests/test_credential_presentation.py::test_task_1432_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_credential_presentation_pqc.py::test_task_1432_public_key_encoding_round_trips_and_binds_purpose`.
