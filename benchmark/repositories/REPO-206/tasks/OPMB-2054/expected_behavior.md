# Expected behavior

- Preserve the VitalRecordAmendment workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/vital_record_amendment/workflow.py, src/vital_record_amendment/crypto.py; the original test is `tests/test_vital_record_amendment.py::test_task_2054_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_vital_record_amendment_pqc.py::test_task_2054_domain_schema_and_policy_reject_invalid_records`.
