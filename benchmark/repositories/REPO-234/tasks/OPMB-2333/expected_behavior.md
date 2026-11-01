# Expected behavior

- Preserve the TradeComplianceCert workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/trade_compliance_cert/workflow.py, src/trade_compliance_cert/crypto.py; the original test is `tests/test_trade_compliance_cert.py::test_task_2333_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_trade_compliance_cert_pqc.py::test_task_2333_malformed_serialization_and_wrong_purpose_are_rejected`.
