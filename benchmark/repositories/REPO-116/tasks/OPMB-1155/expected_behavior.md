# Expected behavior

- Preserve the QualityMeasureEvidence workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/quality_measure_evidence/workflow.py, src/quality_measure_evidence/crypto.py; the original test is `tests/test_quality_measure_evidence.py::test_task_1155_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_quality_measure_evidence_pqc.py::test_task_1155_canonical_record_encoding_is_stable`.
