# Expected behavior

- Preserve the RemitAdvice workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/remit_advice/workflow.py, src/remit_advice/crypto.py; the original test is `tests/test_remit_advice.py::test_task_0836_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_remit_advice_pqc.py::test_task_0836_signature_binds_record_context_and_validity`.
