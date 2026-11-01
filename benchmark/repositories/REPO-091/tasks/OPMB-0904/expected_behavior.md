# Expected behavior

- Preserve the LabSpecimenChain workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/lab_specimen_chain/workflow.py, src/lab_specimen_chain/crypto.py; the original test is `tests/test_lab_specimen_chain.py::test_task_0904_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_lab_specimen_chain_pqc.py::test_task_0904_domain_schema_and_policy_reject_invalid_records`.
