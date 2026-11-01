# Expected behavior

- Preserve the ReturnAuthorization workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/return_authorization/workflow.py, src/return_authorization/crypto.py; the original test is `tests/test_return_authorization.py::test_task_2186_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_return_authorization_pqc.py::test_task_2186_signature_binds_record_context_and_validity`.
