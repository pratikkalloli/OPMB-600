# Expected behavior

- Preserve the ProductRecallNotice workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/product_recall_notice/workflow.py, src/product_recall_notice/crypto.py; the original test is `tests/test_product_recall_notice.py::test_task_2283_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_product_recall_notice_pqc.py::test_task_2283_malformed_serialization_and_wrong_purpose_are_rejected`.
