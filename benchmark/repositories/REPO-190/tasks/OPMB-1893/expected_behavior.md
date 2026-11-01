# Expected behavior

- Preserve the DisclosureRedaction workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/disclosure_redaction/workflow.py, src/disclosure_redaction/crypto.py; the original test is `tests/test_disclosure_redaction.py::test_task_1893_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_disclosure_redaction_pqc.py::test_task_1893_malformed_serialization_and_wrong_purpose_are_rejected`.
