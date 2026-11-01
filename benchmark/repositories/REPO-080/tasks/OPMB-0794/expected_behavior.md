# Expected behavior

- Preserve the CreditOffer workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/credit_offer/workflow.py, src/credit_offer/crypto.py; the original test is `tests/test_credit_offer.py::test_task_0794_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_credit_offer_pqc.py::test_task_0794_domain_schema_and_policy_reject_invalid_records`.
