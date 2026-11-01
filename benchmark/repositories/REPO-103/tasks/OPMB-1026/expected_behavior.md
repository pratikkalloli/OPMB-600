# Expected behavior

- Preserve the BloodProductTrace workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/blood_product_trace/workflow.py, src/blood_product_trace/crypto.py; the original test is `tests/test_blood_product_trace.py::test_task_1026_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_blood_product_trace_pqc.py::test_task_1026_signature_binds_record_context_and_validity`.
