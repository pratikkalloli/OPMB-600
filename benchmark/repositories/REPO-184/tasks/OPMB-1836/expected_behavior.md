# Expected behavior

- Preserve the CourtOrderNotice workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/court_order_notice/workflow.py, src/court_order_notice/crypto.py; the original test is `tests/test_court_order_notice.py::test_task_1836_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_court_order_notice_pqc.py::test_task_1836_signature_binds_record_context_and_validity`.
