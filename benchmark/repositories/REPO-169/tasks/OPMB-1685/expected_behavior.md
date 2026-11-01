# Expected behavior

- Preserve the MicrocredentialIssue workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/microcredential_issue/workflow.py, src/microcredential_issue/crypto.py; the original test is `tests/test_microcredential_issue.py::test_task_1685_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_microcredential_issue_pqc.py::test_task_1685_canonical_record_encoding_is_stable`.
