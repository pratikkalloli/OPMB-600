# Expected behavior

- Preserve the CredentialStatusList workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/credential_status_list/workflow.py, src/credential_status_list/crypto.py; the original test is `tests/test_credential_status_list.py::test_task_1316_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_credential_status_list_pqc.py::test_task_1316_signature_binds_record_context_and_validity`.
