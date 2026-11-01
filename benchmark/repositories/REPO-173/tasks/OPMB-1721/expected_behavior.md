# Expected behavior

- Preserve the PublicationCorrection workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/publication_correction/workflow.py, src/publication_correction/crypto.py; the original test is `tests/test_publication_correction.py::test_task_1721_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_publication_correction_pqc.py::test_task_1721_identity_separates_signing_and_transport_keys`.
