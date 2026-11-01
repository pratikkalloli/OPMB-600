# Expected behavior

- Preserve the ResearchCodeArchive workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/research_code_archive/workflow.py, src/research_code_archive/crypto.py; the original test is `tests/test_research_code_archive.py::test_task_1761_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_research_code_archive_pqc.py::test_task_1761_identity_separates_signing_and_transport_keys`.
