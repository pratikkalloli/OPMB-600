# Expected behavior

- Preserve the DisclosureRedaction workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/disclosure_redaction/workflow.py, src/disclosure_redaction/crypto.py; the original test is `tests/test_disclosure_redaction.py::test_task_1897_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_disclosure_redaction_pqc.py::test_task_1897_signature_rejects_tamper_wrong_key_and_downgrade`.
