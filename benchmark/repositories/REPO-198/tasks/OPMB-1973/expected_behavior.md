# Expected behavior

- Preserve the AdminAppeal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/admin_appeal/workflow.py, src/admin_appeal/crypto.py; the original test is `tests/test_admin_appeal.py::test_task_1973_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_admin_appeal_pqc.py::test_task_1973_malformed_serialization_and_wrong_purpose_are_rejected`.
