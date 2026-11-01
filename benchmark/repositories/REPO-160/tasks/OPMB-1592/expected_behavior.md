# Expected behavior

- Preserve the GrantMilestone workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/grant_milestone/workflow.py, src/grant_milestone/crypto.py; the original test is `tests/test_grant_milestone.py::test_task_1592_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_grant_milestone_pqc.py::test_task_1592_public_key_encoding_round_trips_and_binds_purpose`.
