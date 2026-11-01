# Expected behavior

- Preserve the RecordsRequestResponse workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/records_request_response/workflow.py, src/records_request_response/crypto.py; the original test is `tests/test_records_request_response.py::test_task_1924_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_records_request_response_pqc.py::test_task_1924_domain_schema_and_policy_reject_invalid_records`.
