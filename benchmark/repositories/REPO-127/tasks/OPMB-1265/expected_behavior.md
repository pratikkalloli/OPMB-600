# Expected behavior

- Preserve the DelegationGrant workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/delegation_grant/workflow.py, src/delegation_grant/crypto.py; the original test is `tests/test_delegation_grant.py::test_task_1265_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_delegation_grant_pqc.py::test_task_1265_canonical_record_encoding_is_stable`.
