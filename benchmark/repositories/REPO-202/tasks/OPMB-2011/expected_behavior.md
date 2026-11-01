# Expected behavior

- Preserve the BenefitsDecision workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/benefits_decision/workflow.py, src/benefits_decision/crypto.py; the original test is `tests/test_benefits_decision.py::test_task_2011_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_benefits_decision_pqc.py::test_task_2011_identity_separates_signing_and_transport_keys`.
