# Expected behavior

- Preserve the DigitalGoodsLicense workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/digital_goods_license/workflow.py, src/digital_goods_license/crypto.py; the original test is `tests/test_digital_goods_license.py::test_task_2397_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_digital_goods_license_pqc.py::test_task_2397_signature_rejects_tamper_wrong_key_and_downgrade`.
