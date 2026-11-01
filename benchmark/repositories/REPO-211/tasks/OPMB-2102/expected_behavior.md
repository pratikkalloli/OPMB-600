# Expected behavior

- Preserve the RetailOrderAck workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/retail_order_ack/workflow.py, src/retail_order_ack/crypto.py; the original test is `tests/test_retail_order_ack.py::test_task_2102_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_retail_order_ack_pqc.py::test_task_2102_public_key_encoding_round_trips_and_binds_purpose`.
