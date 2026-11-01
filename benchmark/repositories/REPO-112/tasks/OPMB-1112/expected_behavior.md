# Expected behavior

- Preserve the SurgicalChecklist workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/surgical_checklist/workflow.py, src/surgical_checklist/crypto.py; the original test is `tests/test_surgical_checklist.py::test_task_1112_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_surgical_checklist_pqc.py::test_task_1112_public_key_encoding_round_trips_and_binds_purpose`.
