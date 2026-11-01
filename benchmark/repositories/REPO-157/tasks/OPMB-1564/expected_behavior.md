# Expected behavior

- Preserve the ThesisDeposit workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/thesis_deposit/workflow.py, src/thesis_deposit/crypto.py; the original test is `tests/test_thesis_deposit.py::test_task_1564_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_thesis_deposit_pqc.py::test_task_1564_domain_schema_and_policy_reject_invalid_records`.
