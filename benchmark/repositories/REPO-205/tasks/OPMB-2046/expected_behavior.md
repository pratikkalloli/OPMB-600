# Expected behavior

- Preserve the ArchivesTransfer workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/archives_transfer/workflow.py, src/archives_transfer/crypto.py; the original test is `tests/test_archives_transfer.py::test_task_2046_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_archives_transfer_pqc.py::test_task_2046_signature_binds_record_context_and_validity`.
