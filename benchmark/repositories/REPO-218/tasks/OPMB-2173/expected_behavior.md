# Expected behavior

- Preserve the PartnerOrderExchange workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/partner_order_exchange/workflow.py, src/partner_order_exchange/crypto.py; the original test is `tests/test_partner_order_exchange.py::test_task_2173_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_partner_order_exchange_pqc.py::test_task_2173_malformed_serialization_and_wrong_purpose_are_rejected`.
