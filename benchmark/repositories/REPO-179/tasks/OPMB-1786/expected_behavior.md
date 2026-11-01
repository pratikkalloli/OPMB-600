# Expected behavior

- Preserve the LearningWallet workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/learning_wallet/workflow.py, src/learning_wallet/crypto.py; the original test is `tests/test_learning_wallet.py::test_task_1786_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_learning_wallet_pqc.py::test_task_1786_signature_binds_record_context_and_validity`.
