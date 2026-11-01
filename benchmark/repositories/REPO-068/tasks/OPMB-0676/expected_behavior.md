# Expected behavior

- Preserve the CollateralRegister workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/collateral_register/workflow.py, src/collateral_register/crypto.py; the original test is `tests/test_collateral_register.py::test_task_0676_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_collateral_register_pqc.py::test_task_0676_signature_binds_record_context_and_validity`.
