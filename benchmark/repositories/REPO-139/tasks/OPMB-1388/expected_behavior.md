# Expected behavior

- Preserve the TrustPolicyRelease workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/trust_policy_release/workflow.py, src/trust_policy_release/crypto.py; the original test is `tests/test_trust_policy_release.py::test_task_1388_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_trust_policy_release_pqc.py::test_task_1388_hybrid_envelope_binds_recipient_and_record_context`.
