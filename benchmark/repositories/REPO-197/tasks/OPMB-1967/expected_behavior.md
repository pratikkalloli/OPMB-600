# Expected behavior

- Preserve the DocketSnapshot workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/docket_snapshot/workflow.py, src/docket_snapshot/crypto.py; the original test is `tests/test_docket_snapshot.py::test_task_1967_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_docket_snapshot_pqc.py::test_task_1967_signature_rejects_tamper_wrong_key_and_downgrade`.
