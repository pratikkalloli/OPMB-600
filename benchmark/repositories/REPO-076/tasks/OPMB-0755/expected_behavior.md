# Expected behavior

- Preserve the TreasurySignal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/treasury_signal/workflow.py, src/treasury_signal/crypto.py; the original test is `tests/test_treasury_signal.py::test_task_0755_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_treasury_signal_pqc.py::test_task_0755_canonical_record_encoding_is_stable`.
