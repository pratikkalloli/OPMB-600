# Expected behavior

- Preserve the RevocationWitness workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/revocation_witness/workflow.py, src/revocation_witness/crypto.py; the original test is `tests/test_revocation_witness.py::test_task_1242_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_revocation_witness_pqc.py::test_task_1242_public_key_encoding_round_trips_and_binds_purpose`.
