# Expected behavior

- Preserve the RootKeySuccession workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/root_key_succession/workflow.py, src/root_key_succession/crypto.py; the original test is `tests/test_root_key_succession.py::test_task_1475_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_root_key_succession_pqc.py::test_task_1475_canonical_record_encoding_is_stable`.
