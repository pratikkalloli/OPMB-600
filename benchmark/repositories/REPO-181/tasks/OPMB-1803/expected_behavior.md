# Expected behavior

- Preserve the EvidenceCustodyChain workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/evidence_custody_chain/workflow.py, src/evidence_custody_chain/crypto.py; the original test is `tests/test_evidence_custody_chain.py::test_task_1803_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_evidence_custody_chain_pqc.py::test_task_1803_malformed_serialization_and_wrong_purpose_are_rejected`.
