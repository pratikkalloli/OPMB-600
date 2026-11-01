# Expected behavior

- Preserve the TrustAnchorRoll workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/trust_anchor_roll/workflow.py, src/trust_anchor_roll/crypto.py; the original test is `tests/test_trust_anchor_roll.py::test_task_1228_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_trust_anchor_roll_pqc.py::test_task_1228_hybrid_envelope_binds_recipient_and_record_context`.
