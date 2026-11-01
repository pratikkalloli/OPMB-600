# Expected behavior

- Preserve the LegalHoldNotice workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/legal_hold_notice/workflow.py, src/legal_hold_notice/crypto.py; the original test is `tests/test_legal_hold_notice.py::test_task_1996_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_legal_hold_notice_pqc.py::test_task_1996_signature_binds_record_context_and_validity`.
