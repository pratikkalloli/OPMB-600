# Expected behavior

- Preserve the CrossBorderIdentity workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/cross_border_identity/workflow.py, src/cross_border_identity/crypto.py; the original test is `tests/test_cross_border_identity.py::test_task_1458_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_cross_border_identity_pqc.py::test_task_1458_hybrid_envelope_binds_recipient_and_record_context`.
