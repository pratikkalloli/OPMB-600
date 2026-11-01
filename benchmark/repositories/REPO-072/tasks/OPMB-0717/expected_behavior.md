# Expected behavior

- Preserve the ReinsuranceSlip workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/reinsurance_slip/workflow.py, src/reinsurance_slip/crypto.py; the original test is `tests/test_reinsurance_slip.py::test_task_0717_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_reinsurance_slip_pqc.py::test_task_0717_signature_rejects_tamper_wrong_key_and_downgrade`.
