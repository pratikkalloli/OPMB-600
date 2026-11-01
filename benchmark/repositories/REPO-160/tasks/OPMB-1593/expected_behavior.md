# Expected behavior

- Preserve the GrantMilestone workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/grant_milestone/workflow.py, src/grant_milestone/crypto.py; the original test is `tests/test_grant_milestone.py::test_task_1593_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_grant_milestone_pqc.py::test_task_1593_malformed_serialization_and_wrong_purpose_are_rejected`.
