# Expected behavior

- Preserve the AgeCredential workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/age_credential/workflow.py, src/age_credential/crypto.py; the original test is `tests/test_age_credential.py::test_task_1355_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_age_credential_pqc.py::test_task_1355_canonical_record_encoding_is_stable`.
