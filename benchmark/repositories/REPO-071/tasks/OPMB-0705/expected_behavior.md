# Expected behavior

- Preserve the PolicyAmendment workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/policy_amendment/workflow.py, src/policy_amendment/crypto.py; the original test is `tests/test_policy_amendment.py::test_task_0705_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_policy_amendment_pqc.py::test_task_0705_canonical_record_encoding_is_stable`.
