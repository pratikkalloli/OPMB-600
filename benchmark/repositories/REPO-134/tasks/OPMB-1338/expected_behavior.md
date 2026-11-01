# Expected behavior

- Preserve the ResidencyCredential workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/residency_credential/workflow.py, src/residency_credential/crypto.py; the original test is `tests/test_residency_credential.py::test_task_1338_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_residency_credential_pqc.py::test_task_1338_hybrid_envelope_binds_recipient_and_record_context`.
