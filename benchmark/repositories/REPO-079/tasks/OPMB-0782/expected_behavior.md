# Expected behavior

- Preserve the TaxRemit workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/tax_remit/workflow.py, src/tax_remit/crypto.py; the original test is `tests/test_tax_remit.py::test_task_0782_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_tax_remit_pqc.py::test_task_0782_public_key_encoding_round_trips_and_binds_purpose`.
