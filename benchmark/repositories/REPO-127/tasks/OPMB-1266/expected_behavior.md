# Expected behavior

- Preserve the DelegationGrant workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/delegation_grant/workflow.py, src/delegation_grant/crypto.py; the original test is `tests/test_delegation_grant.py::test_task_1266_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_delegation_grant_pqc.py::test_task_1266_signature_binds_record_context_and_validity`.
