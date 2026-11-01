# Expected behavior

- Preserve the TreasurySignal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/treasury_signal/workflow.py, src/treasury_signal/crypto.py; the original test is `tests/test_treasury_signal.py::test_task_0752_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_treasury_signal_pqc.py::test_task_0752_public_key_encoding_round_trips_and_binds_purpose`.
