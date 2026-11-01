# Expected behavior

- Preserve the LegislativeVoteRecord workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/legislative_vote_record/workflow.py, src/legislative_vote_record/crypto.py; the original test is `tests/test_legislative_vote_record.py::test_task_2069_rotation_retires_old_key_version` and PQC migration test is `tests/test_legislative_vote_record_pqc.py::test_task_2069_rotation_retires_old_key_version`.
