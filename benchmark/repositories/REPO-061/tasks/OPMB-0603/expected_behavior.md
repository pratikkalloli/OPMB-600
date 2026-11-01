# Expected behavior

- Preserve the MandateFlow workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/mandate_flow/workflow.py, src/mandate_flow/crypto.py; the original test is `tests/test_mandate_flow.py::test_task_0603_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_mandate_flow_pqc.py::test_task_0603_malformed_serialization_and_wrong_purpose_are_rejected`.
