# Expected behavior

- Preserve the RadiologyPeerReview workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/radiology_peer_review/workflow.py, src/radiology_peer_review/crypto.py; the original test is `tests/test_radiology_peer_review.py::test_task_1128_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_radiology_peer_review_pqc.py::test_task_1128_hybrid_envelope_binds_recipient_and_record_context`.
