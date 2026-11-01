# Expected behavior

- Preserve the CollateralRegister workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/collateral_register/workflow.py, src/collateral_register/crypto.py; the original test is `tests/test_collateral_register.py::test_task_0678_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_collateral_register_pqc.py::test_task_0678_hybrid_envelope_binds_recipient_and_record_context`.
