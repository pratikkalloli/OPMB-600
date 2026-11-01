# Expected behavior

- Preserve the CollateralRegister workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/collateral_register/workflow.py, src/collateral_register/crypto.py; the original test is `tests/test_collateral_register.py::test_task_0672_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_collateral_register_pqc.py::test_task_0672_public_key_encoding_round_trips_and_binds_purpose`.
