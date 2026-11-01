# Expected behavior

- Preserve the ImagingReadoutSign workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/imaging_readout_sign/workflow.py, src/imaging_readout_sign/crypto.py; the original test is `tests/test_imaging_readout_sign.py::test_task_0912_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_imaging_readout_sign_pqc.py::test_task_0912_public_key_encoding_round_trips_and_binds_purpose`.
