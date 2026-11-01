# Expected behavior

- Preserve the LabNotebookSeal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/lab_notebook_seal/workflow.py, src/lab_notebook_seal/crypto.py; the original test is `tests/test_lab_notebook_seal.py::test_task_1605_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_lab_notebook_seal_pqc.py::test_task_1605_canonical_record_encoding_is_stable`.
