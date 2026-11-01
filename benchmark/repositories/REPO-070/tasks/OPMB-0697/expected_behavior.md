# Expected behavior

- Preserve the PremiumNotice workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/premium_notice/workflow.py, src/premium_notice/crypto.py; the original test is `tests/test_premium_notice.py::test_task_0697_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_premium_notice_pqc.py::test_task_0697_signature_rejects_tamper_wrong_key_and_downgrade`.
