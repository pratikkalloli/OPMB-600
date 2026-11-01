# Expected behavior

- Preserve the AuthenticatorBinding workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/authenticator_binding/workflow.py, src/authenticator_binding/crypto.py; the original test is `tests/test_authenticator_binding.py::test_task_1288_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_authenticator_binding_pqc.py::test_task_1288_hybrid_envelope_binds_recipient_and_record_context`.
