# Expected behavior

- Preserve the SelectiveDisclosure workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/selective_disclosure/workflow.py, src/selective_disclosure/crypto.py; the original test is `tests/test_selective_disclosure.py::test_task_1444_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_selective_disclosure_pqc.py::test_task_1444_domain_schema_and_policy_reject_invalid_records`.
