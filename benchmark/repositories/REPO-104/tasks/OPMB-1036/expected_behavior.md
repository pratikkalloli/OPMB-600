# Expected behavior

- Preserve the PathologyResult workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/pathology_result/workflow.py, src/pathology_result/crypto.py; the original test is `tests/test_pathology_result.py::test_task_1036_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_pathology_result_pqc.py::test_task_1036_signature_binds_record_context_and_validity`.
