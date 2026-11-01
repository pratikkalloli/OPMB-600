# Expected behavior

- Preserve the ServiceOfProcess workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/service_of_process/workflow.py, src/service_of_process/crypto.py; the original test is `tests/test_service_of_process.py::test_task_2081_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_service_of_process_pqc.py::test_task_2081_identity_separates_signing_and_transport_keys`.
