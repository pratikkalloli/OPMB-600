# Expected behavior

- Preserve the DepositionTranscript workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/deposition_transcript/workflow.py, src/deposition_transcript/crypto.py; the original test is `tests/test_deposition_transcript.py::test_task_2008_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_deposition_transcript_pqc.py::test_task_2008_hybrid_envelope_binds_recipient_and_record_context`.
