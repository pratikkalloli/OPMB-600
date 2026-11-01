# Expected behavior

- Preserve the OrdinancePublication workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/ordinance_publication/workflow.py, src/ordinance_publication/crypto.py; the original test is `tests/test_ordinance_publication.py::test_task_1953_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_ordinance_publication_pqc.py::test_task_1953_malformed_serialization_and_wrong_purpose_are_rejected`.
