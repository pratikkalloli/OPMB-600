# Expected behavior

- Preserve the TradeComplianceCert workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/trade_compliance_cert/workflow.py, src/trade_compliance_cert/crypto.py; the original test is `tests/test_trade_compliance_cert.py::test_task_2332_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_trade_compliance_cert_pqc.py::test_task_2332_public_key_encoding_round_trips_and_binds_purpose`.
