# Expected behavior

- Preserve the LoyaltyPointTransfer workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/loyalty_point_transfer/workflow.py, src/loyalty_point_transfer/crypto.py; the original test is `tests/test_loyalty_point_transfer.py::test_task_2215_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_loyalty_point_transfer_pqc.py::test_task_2215_canonical_record_encoding_is_stable`.
