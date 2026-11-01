# Expected behavior

- Preserve the PartnerOrderExchange workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/partner_order_exchange/workflow.py, src/partner_order_exchange/crypto.py; the original test is `tests/test_partner_order_exchange.py::test_task_2174_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_partner_order_exchange_pqc.py::test_task_2174_domain_schema_and_policy_reject_invalid_records`.
