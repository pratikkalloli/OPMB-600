# Expected behavior

- Preserve the TranscriptSeal workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/transcript_seal/workflow.py, src/transcript_seal/crypto.py; the original test is `tests/test_transcript_seal.py::test_task_1503_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_transcript_seal_pqc.py::test_task_1503_malformed_serialization_and_wrong_purpose_are_rejected`.
