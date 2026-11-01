# Expected behavior

- Preserve the JurySummons workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/jury_summons/workflow.py, src/jury_summons/crypto.py; the original test is `tests/test_jury_summons.py::test_task_1901_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_jury_summons_pqc.py::test_task_1901_identity_separates_signing_and_transport_keys`.
