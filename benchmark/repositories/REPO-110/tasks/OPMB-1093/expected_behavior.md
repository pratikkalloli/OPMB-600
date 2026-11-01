# Expected behavior

- Preserve the AdverseEventReport workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/adverse_event_report/workflow.py, src/adverse_event_report/crypto.py; the original test is `tests/test_adverse_event_report.py::test_task_1093_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_adverse_event_report_pqc.py::test_task_1093_malformed_serialization_and_wrong_purpose_are_rejected`.
