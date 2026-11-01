# Expected behavior

- Preserve the CarePlanRevision workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/care_plan_revision/workflow.py, src/care_plan_revision/crypto.py; the original test is `tests/test_care_plan_revision.py::test_task_1043_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_care_plan_revision_pqc.py::test_task_1043_malformed_serialization_and_wrong_purpose_are_rejected`.
