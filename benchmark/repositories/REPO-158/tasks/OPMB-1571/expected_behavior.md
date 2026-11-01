# Expected behavior

- Preserve the PeerReviewCloseout workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/peer_review_closeout/workflow.py, src/peer_review_closeout/crypto.py; the original test is `tests/test_peer_review_closeout.py::test_task_1571_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_peer_review_closeout_pqc.py::test_task_1571_identity_separates_signing_and_transport_keys`.
