# Expected behavior

- Preserve the LandTitleTransfer workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/land_title_transfer/workflow.py, src/land_title_transfer/crypto.py; the original test is `tests/test_land_title_transfer.py::test_task_1878_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_land_title_transfer_pqc.py::test_task_1878_hybrid_envelope_binds_recipient_and_record_context`.
