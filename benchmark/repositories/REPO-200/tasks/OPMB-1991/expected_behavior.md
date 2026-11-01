# Expected behavior

- Preserve the LegalHoldNotice workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/legal_hold_notice/workflow.py, src/legal_hold_notice/crypto.py; the original test is `tests/test_legal_hold_notice.py::test_task_1991_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_legal_hold_notice_pqc.py::test_task_1991_identity_separates_signing_and_transport_keys`.
