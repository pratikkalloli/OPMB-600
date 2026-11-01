# Expected behavior

- Preserve the DischargeDigest workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/discharge_digest/workflow.py, src/discharge_digest/crypto.py; the original test is `tests/test_discharge_digest.py::test_task_0946_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_discharge_digest_pqc.py::test_task_0946_signature_binds_record_context_and_validity`.
