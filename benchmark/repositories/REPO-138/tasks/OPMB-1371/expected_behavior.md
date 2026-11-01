# Expected behavior

- Preserve the KeyCeremonyRecord workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/key_ceremony_record/workflow.py, src/key_ceremony_record/crypto.py; the original test is `tests/test_key_ceremony_record.py::test_task_1371_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_key_ceremony_record_pqc.py::test_task_1371_identity_separates_signing_and_transport_keys`.
