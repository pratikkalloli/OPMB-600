# Expected behavior

- Preserve the ProceedingRelease workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/proceeding_release/workflow.py, src/proceeding_release/crypto.py; the original test is `tests/test_proceeding_release.py::test_task_1677_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_proceeding_release_pqc.py::test_task_1677_signature_rejects_tamper_wrong_key_and_downgrade`.
