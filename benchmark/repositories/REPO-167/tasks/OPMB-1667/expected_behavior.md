# Expected behavior

- Preserve the CitationCorrection workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/citation_correction/workflow.py, src/citation_correction/crypto.py; the original test is `tests/test_citation_correction.py::test_task_1667_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_citation_correction_pqc.py::test_task_1667_signature_rejects_tamper_wrong_key_and_downgrade`.
