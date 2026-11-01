# Expected behavior

- Preserve the MarketplacePayout workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/marketplace_payout/workflow.py, src/marketplace_payout/crypto.py; the original test is `tests/test_marketplace_payout.py::test_task_2252_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_marketplace_payout_pqc.py::test_task_2252_public_key_encoding_round_trips_and_binds_purpose`.
