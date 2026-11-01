# Expected behavior

- Preserve the IssuerAccreditation workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/issuer_accreditation/workflow.py, src/issuer_accreditation/crypto.py; the original test is `tests/test_issuer_accreditation.py::test_task_1305_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_issuer_accreditation_pqc.py::test_task_1305_canonical_record_encoding_is_stable`.
