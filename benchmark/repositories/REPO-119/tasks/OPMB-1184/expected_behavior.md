# Expected behavior

- Preserve the PharmaBatchTrace workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/pharma_batch_trace/workflow.py, src/pharma_batch_trace/crypto.py; the original test is `tests/test_pharma_batch_trace.py::test_task_1184_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_pharma_batch_trace_pqc.py::test_task_1184_domain_schema_and_policy_reject_invalid_records`.
