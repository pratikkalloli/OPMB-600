# Expected behavior

- Preserve the DeviceCalibrationLog workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/device_calibration_log/workflow.py, src/device_calibration_log/crypto.py; the original test is `tests/test_device_calibration_log.py::test_task_0996_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_device_calibration_log_pqc.py::test_task_0996_signature_binds_record_context_and_validity`.
