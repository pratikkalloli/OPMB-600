# Expected behavior

- Preserve the ProceedingRelease workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/proceeding_release/workflow.py, src/proceeding_release/crypto.py; the original test is `tests/test_proceeding_release.py::test_task_1671_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_proceeding_release_pqc.py::test_task_1671_identity_separates_signing_and_transport_keys`.
