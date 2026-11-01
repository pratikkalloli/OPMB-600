# Expected behavior

- Preserve the PathologyResult workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/pathology_result/workflow.py, src/pathology_result/crypto.py; the original test is `tests/test_pathology_result.py::test_task_1035_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_pathology_result_pqc.py::test_task_1035_canonical_record_encoding_is_stable`.
