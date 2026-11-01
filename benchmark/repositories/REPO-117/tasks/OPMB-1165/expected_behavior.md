# Expected behavior

- Preserve the InteropSchemaRelease workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/interop_schema_release/workflow.py, src/interop_schema_release/crypto.py; the original test is `tests/test_interop_schema_release.py::test_task_1165_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_interop_schema_release_pqc.py::test_task_1165_canonical_record_encoding_is_stable`.
