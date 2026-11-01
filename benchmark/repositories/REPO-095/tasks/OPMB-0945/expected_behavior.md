# Expected behavior

- Preserve the DischargeDigest workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/discharge_digest/workflow.py, src/discharge_digest/crypto.py; the original test is `tests/test_discharge_digest.py::test_task_0945_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_discharge_digest_pqc.py::test_task_0945_canonical_record_encoding_is_stable`.
