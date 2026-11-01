# Expected behavior

- Preserve the CitationCorrection workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/citation_correction/workflow.py, src/citation_correction/crypto.py; the original test is `tests/test_citation_correction.py::test_task_1666_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_citation_correction_pqc.py::test_task_1666_signature_binds_record_context_and_validity`.
