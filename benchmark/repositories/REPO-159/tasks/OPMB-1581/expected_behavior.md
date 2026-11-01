# Expected behavior

- Preserve the InstrumentCalibration workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/instrument_calibration/workflow.py, src/instrument_calibration/crypto.py; the original test is `tests/test_instrument_calibration.py::test_task_1581_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_instrument_calibration_pqc.py::test_task_1581_identity_separates_signing_and_transport_keys`.
