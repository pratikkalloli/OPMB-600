# Expected behavior

- Preserve the B2BRebateClaim workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/b2_b_rebate_claim/workflow.py, src/b2_b_rebate_claim/crypto.py; the original test is `tests/test_b2_b_rebate_claim.py::test_task_2322_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_b2_b_rebate_claim_pqc.py::test_task_2322_public_key_encoding_round_trips_and_binds_purpose`.
