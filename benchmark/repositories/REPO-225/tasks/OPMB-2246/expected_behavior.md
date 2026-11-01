# Expected behavior

- Preserve the SubscriptionRenewal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/subscription_renewal/workflow.py, src/subscription_renewal/crypto.py; the original test is `tests/test_subscription_renewal.py::test_task_2246_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_subscription_renewal_pqc.py::test_task_2246_signature_binds_record_context_and_validity`.
