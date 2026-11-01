# Expected behavior

- Preserve the CivicIdCredential workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/civic_id_credential/workflow.py, src/civic_id_credential/crypto.py; the original test is `tests/test_civic_id_credential.py::test_task_1205_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_civic_id_credential_pqc.py::test_task_1205_canonical_record_encoding_is_stable`.
