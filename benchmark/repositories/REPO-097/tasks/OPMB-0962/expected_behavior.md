# Expected behavior

- Preserve the ResearchCohortExport workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/research_cohort_export/workflow.py, src/research_cohort_export/crypto.py; the original test is `tests/test_research_cohort_export.py::test_task_0962_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_research_cohort_export_pqc.py::test_task_0962_public_key_encoding_round_trips_and_binds_purpose`.
