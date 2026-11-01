# Expected behavior

- Preserve the TradeComplianceCert workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/trade_compliance_cert/workflow.py, src/trade_compliance_cert/crypto.py; the original test is `tests/test_trade_compliance_cert.py::test_task_2336_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_trade_compliance_cert_pqc.py::test_task_2336_signature_binds_record_context_and_validity`.
