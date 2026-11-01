# Expected behavior

- Preserve the ClaimEvidence workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/claim_evidence/workflow.py, src/claim_evidence/crypto.py; the original test is `tests/test_claim_evidence.py::test_task_0682_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_claim_evidence_pqc.py::test_task_0682_public_key_encoding_round_trips_and_binds_purpose`.
