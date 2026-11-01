# Expected behavior

- Preserve the CivicPetition workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/civic_petition/workflow.py, src/civic_petition/crypto.py; the original test is `tests/test_civic_petition.py::test_task_1932_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_civic_petition_pqc.py::test_task_1932_public_key_encoding_round_trips_and_binds_purpose`.
