# Expected behavior

- Preserve the BrokerOrder workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/broker_order/workflow.py, src/broker_order/crypto.py; the original test is `tests/test_broker_order.py::test_task_0727_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_broker_order_pqc.py::test_task_0727_signature_rejects_tamper_wrong_key_and_downgrade`.
