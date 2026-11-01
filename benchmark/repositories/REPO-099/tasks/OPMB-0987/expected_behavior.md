# Expected behavior

- Preserve the GenomicReportSeal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/genomic_report_seal/workflow.py, src/genomic_report_seal/crypto.py; the original test is `tests/test_genomic_report_seal.py::test_task_0987_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_genomic_report_seal_pqc.py::test_task_0987_signature_rejects_tamper_wrong_key_and_downgrade`.
