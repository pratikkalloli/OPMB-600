# Expected behavior

- Preserve the FranchiseRoyaltyReport workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/franchise_royalty_report/workflow.py, src/franchise_royalty_report/crypto.py; the original test is `tests/test_franchise_royalty_report.py::test_task_2358_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_franchise_royalty_report_pqc.py::test_task_2358_hybrid_envelope_binds_recipient_and_record_context`.
