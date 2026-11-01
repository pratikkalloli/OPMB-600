# Expected behavior

- Preserve the PublicMinutes workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/public_minutes/workflow.py, src/public_minutes/crypto.py; the original test is `tests/test_public_minutes.py::test_task_1846_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_public_minutes_pqc.py::test_task_1846_signature_binds_record_context_and_validity`.
