# Expected behavior

- Preserve the StatuteAmendment workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/statute_amendment/workflow.py, src/statute_amendment/crypto.py; the original test is `tests/test_statute_amendment.py::test_task_1853_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_statute_amendment_pqc.py::test_task_1853_malformed_serialization_and_wrong_purpose_are_rejected`.
