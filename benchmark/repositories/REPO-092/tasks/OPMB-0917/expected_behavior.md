# Expected behavior

- Preserve the ImagingReadoutSign workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/imaging_readout_sign/workflow.py, src/imaging_readout_sign/crypto.py; the original test is `tests/test_imaging_readout_sign.py::test_task_0917_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_imaging_readout_sign_pqc.py::test_task_0917_signature_rejects_tamper_wrong_key_and_downgrade`.
