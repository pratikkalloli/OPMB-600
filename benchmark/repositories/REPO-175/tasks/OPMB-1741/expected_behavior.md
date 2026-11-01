# Expected behavior

- Preserve the ResearchEthicsDecision workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/research_ethics_decision/workflow.py, src/research_ethics_decision/crypto.py; the original test is `tests/test_research_ethics_decision.py::test_task_1741_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_research_ethics_decision_pqc.py::test_task_1741_identity_separates_signing_and_transport_keys`.
