# Expected behavior

- Preserve the CustodyPositionRecon workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/custody_position_recon/workflow.py, src/custody_position_recon/crypto.py; the original test is `tests/test_custody_position_recon.py::test_task_0749_rotation_retires_old_key_version` and PQC migration test is `tests/test_custody_position_recon_pqc.py::test_task_0749_rotation_retires_old_key_version`.
