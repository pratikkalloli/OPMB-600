# Expected behavior

- Preserve the ReceivableSaleNotice workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/receivable_sale_notice/workflow.py, src/receivable_sale_notice/crypto.py; the original test is `tests/test_receivable_sale_notice.py::test_task_0655_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_receivable_sale_notice_pqc.py::test_task_0655_canonical_record_encoding_is_stable`.
