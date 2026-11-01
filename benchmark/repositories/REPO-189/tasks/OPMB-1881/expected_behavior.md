# Expected behavior

- Preserve the ProcurementBidCommit workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/procurement_bid_commit/workflow.py, src/procurement_bid_commit/crypto.py; the original test is `tests/test_procurement_bid_commit.py::test_task_1881_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_procurement_bid_commit_pqc.py::test_task_1881_identity_separates_signing_and_transport_keys`.
