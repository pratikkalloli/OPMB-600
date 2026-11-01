# Expected behavior

- Preserve the HolderDeviceRecovery workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/holder_device_recovery/workflow.py, src/holder_device_recovery/crypto.py; the original test is `tests/test_holder_device_recovery.py::test_task_1498_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_holder_device_recovery_pqc.py::test_task_1498_hybrid_envelope_binds_recipient_and_record_context`.
