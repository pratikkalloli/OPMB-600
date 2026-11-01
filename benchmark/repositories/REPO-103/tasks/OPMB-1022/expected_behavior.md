# Expected behavior

- Preserve the BloodProductTrace workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/blood_product_trace/workflow.py, src/blood_product_trace/crypto.py; the original test is `tests/test_blood_product_trace.py::test_task_1022_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_blood_product_trace_pqc.py::test_task_1022_public_key_encoding_round_trips_and_binds_purpose`.
