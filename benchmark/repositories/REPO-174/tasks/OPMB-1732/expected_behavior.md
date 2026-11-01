# Expected behavior

- Preserve the DissertationEmbargo workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/dissertation_embargo/workflow.py, src/dissertation_embargo/crypto.py; the original test is `tests/test_dissertation_embargo.py::test_task_1732_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_dissertation_embargo_pqc.py::test_task_1732_public_key_encoding_round_trips_and_binds_purpose`.
