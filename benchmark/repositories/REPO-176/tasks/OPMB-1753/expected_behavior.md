# Expected behavior

- Preserve the LabAccessPass workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/lab_access_pass/workflow.py, src/lab_access_pass/crypto.py; the original test is `tests/test_lab_access_pass.py::test_task_1753_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_lab_access_pass_pqc.py::test_task_1753_malformed_serialization_and_wrong_purpose_are_rejected`.
