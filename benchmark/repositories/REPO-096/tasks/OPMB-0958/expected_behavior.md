# Expected behavior

- Preserve the TrialProtocolRelease workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/trial_protocol_release/workflow.py, src/trial_protocol_release/crypto.py; the original test is `tests/test_trial_protocol_release.py::test_task_0958_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_trial_protocol_release_pqc.py::test_task_0958_hybrid_envelope_binds_recipient_and_record_context`.
