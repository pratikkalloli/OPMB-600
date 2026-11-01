# Expected behavior

- Preserve the PriceBookPublish workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/price_book_publish/workflow.py, src/price_book_publish/crypto.py; the original test is `tests/test_price_book_publish.py::test_task_2194_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_price_book_publish_pqc.py::test_task_2194_domain_schema_and_policy_reject_invalid_records`.
