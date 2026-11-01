# Expected behavior

- Preserve the LabNotebookSeal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/lab_notebook_seal/workflow.py, src/lab_notebook_seal/crypto.py; the original test is `tests/test_lab_notebook_seal.py::test_task_1602_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_lab_notebook_seal_pqc.py::test_task_1602_public_key_encoding_round_trips_and_binds_purpose`.
