# Expected behavior

- Preserve the SelectiveDisclosure workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/selective_disclosure/workflow.py, src/selective_disclosure/crypto.py; the original test is `tests/test_selective_disclosure.py::test_task_1442_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_selective_disclosure_pqc.py::test_task_1442_public_key_encoding_round_trips_and_binds_purpose`.
