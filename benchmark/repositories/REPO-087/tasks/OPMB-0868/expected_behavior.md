# Expected behavior

- Preserve the BondCoupon workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/bond_coupon/workflow.py, src/bond_coupon/crypto.py; the original test is `tests/test_bond_coupon.py::test_task_0868_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_bond_coupon_pqc.py::test_task_0868_hybrid_envelope_binds_recipient_and_record_context`.
