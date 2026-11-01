# Expected behavior

- Preserve the ReinsuranceSlip workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/reinsurance_slip/workflow.py, src/reinsurance_slip/crypto.py; the original test is `tests/test_reinsurance_slip.py::test_task_0719_rotation_retires_old_key_version` and PQC migration test is `tests/test_reinsurance_slip_pqc.py::test_task_0719_rotation_retires_old_key_version`.
