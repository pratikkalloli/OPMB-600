# Expected behavior

- Preserve the ElectionObserver workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/election_observer/workflow.py, src/election_observer/crypto.py; the original test is `tests/test_election_observer.py::test_task_1945_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_election_observer_pqc.py::test_task_1945_canonical_record_encoding_is_stable`.
