# Expected behavior

- Preserve the NotarySeal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/notary_seal/workflow.py, src/notary_seal/crypto.py; the original test is `tests/test_notary_seal.py::test_task_1828_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_notary_seal_pqc.py::test_task_1828_hybrid_envelope_binds_recipient_and_record_context`.
