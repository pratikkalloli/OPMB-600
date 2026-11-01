# Expected behavior

- Preserve the CertRenewalPlan workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/cert_renewal_plan/workflow.py, src/cert_renewal_plan/crypto.py; the original test is `tests/test_cert_renewal_plan.py::test_task_1239_rotation_retires_old_key_version` and PQC migration test is `tests/test_cert_renewal_plan_pqc.py::test_task_1239_rotation_retires_old_key_version`.
