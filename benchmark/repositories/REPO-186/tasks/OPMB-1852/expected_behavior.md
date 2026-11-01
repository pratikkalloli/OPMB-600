# Expected behavior

- Preserve the StatuteAmendment workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/statute_amendment/workflow.py, src/statute_amendment/crypto.py; the original test is `tests/test_statute_amendment.py::test_task_1852_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_statute_amendment_pqc.py::test_task_1852_public_key_encoding_round_trips_and_binds_purpose`.
