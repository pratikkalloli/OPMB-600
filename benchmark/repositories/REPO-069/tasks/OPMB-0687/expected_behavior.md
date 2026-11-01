# Expected behavior

- Preserve the ClaimEvidence workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/claim_evidence/workflow.py, src/claim_evidence/crypto.py; the original test is `tests/test_claim_evidence.py::test_task_0687_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_claim_evidence_pqc.py::test_task_0687_signature_rejects_tamper_wrong_key_and_downgrade`.
