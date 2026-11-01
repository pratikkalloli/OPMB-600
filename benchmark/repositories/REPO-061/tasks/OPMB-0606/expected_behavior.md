# Expected behavior

- Preserve the MandateFlow workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/mandate_flow/workflow.py, src/mandate_flow/crypto.py; the original test is `tests/test_mandate_flow.py::test_task_0606_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_mandate_flow_pqc.py::test_task_0606_signature_binds_record_context_and_validity`.
