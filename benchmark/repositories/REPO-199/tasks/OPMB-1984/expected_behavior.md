# Expected behavior

- Preserve the RegulatoryFiling workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/regulatory_filing/workflow.py, src/regulatory_filing/crypto.py; the original test is `tests/test_regulatory_filing.py::test_task_1984_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_regulatory_filing_pqc.py::test_task_1984_domain_schema_and_policy_reject_invalid_records`.
