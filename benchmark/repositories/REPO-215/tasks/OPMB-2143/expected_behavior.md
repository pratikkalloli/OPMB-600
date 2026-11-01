# Expected behavior

- Preserve the ProductBatchTrace workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/product_batch_trace/workflow.py, src/product_batch_trace/crypto.py; the original test is `tests/test_product_batch_trace.py::test_task_2143_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_product_batch_trace_pqc.py::test_task_2143_malformed_serialization_and_wrong_purpose_are_rejected`.
