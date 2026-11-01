# Expected behavior

- Preserve the AuthenticatorBinding workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/authenticator_binding/workflow.py, src/authenticator_binding/crypto.py; the original test is `tests/test_authenticator_binding.py::test_task_1286_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_authenticator_binding_pqc.py::test_task_1286_signature_binds_record_context_and_validity`.
