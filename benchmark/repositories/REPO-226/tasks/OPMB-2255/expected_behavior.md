# Expected behavior

- Preserve the MarketplacePayout workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/marketplace_payout/workflow.py, src/marketplace_payout/crypto.py; the original test is `tests/test_marketplace_payout.py::test_task_2255_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_marketplace_payout_pqc.py::test_task_2255_canonical_record_encoding_is_stable`.
