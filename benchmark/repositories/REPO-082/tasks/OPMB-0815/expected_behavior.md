# Expected behavior

- Preserve the CardDispute workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/card_dispute/workflow.py, src/card_dispute/crypto.py; the original test is `tests/test_card_dispute.py::test_task_0815_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_card_dispute_pqc.py::test_task_0815_canonical_record_encoding_is_stable`.
