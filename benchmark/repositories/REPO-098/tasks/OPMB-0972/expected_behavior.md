# Expected behavior

- Preserve the BiobankCustody workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/biobank_custody/workflow.py, src/biobank_custody/crypto.py; the original test is `tests/test_biobank_custody.py::test_task_0972_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_biobank_custody_pqc.py::test_task_0972_public_key_encoding_round_trips_and_binds_purpose`.
