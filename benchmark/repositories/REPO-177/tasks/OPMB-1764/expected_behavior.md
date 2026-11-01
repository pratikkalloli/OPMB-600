# Expected behavior

- Preserve the ResearchCodeArchive workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/research_code_archive/workflow.py, src/research_code_archive/crypto.py; the original test is `tests/test_research_code_archive.py::test_task_1764_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_research_code_archive_pqc.py::test_task_1764_domain_schema_and_policy_reject_invalid_records`.
