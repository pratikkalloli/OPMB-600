# Expected behavior

- Preserve the RemitAdvice workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/remit_advice/workflow.py, src/remit_advice/crypto.py; the original test is `tests/test_remit_advice.py::test_task_0832_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_remit_advice_pqc.py::test_task_0832_public_key_encoding_round_trips_and_binds_purpose`.
