# Expected behavior

- Preserve the RadiologyPeerReview workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/radiology_peer_review/workflow.py, src/radiology_peer_review/crypto.py; the original test is `tests/test_radiology_peer_review.py::test_task_1123_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_radiology_peer_review_pqc.py::test_task_1123_malformed_serialization_and_wrong_purpose_are_rejected`.
