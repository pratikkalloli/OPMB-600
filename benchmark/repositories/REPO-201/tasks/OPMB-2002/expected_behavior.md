# Expected behavior

- Preserve the DepositionTranscript workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/deposition_transcript/workflow.py, src/deposition_transcript/crypto.py; the original test is `tests/test_deposition_transcript.py::test_task_2002_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_deposition_transcript_pqc.py::test_task_2002_public_key_encoding_round_trips_and_binds_purpose`.
