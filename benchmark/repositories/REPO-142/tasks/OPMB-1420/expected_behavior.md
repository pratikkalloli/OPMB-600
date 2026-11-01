# Expected behavior

- Preserve the ProofingDecision workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/proofing_decision/workflow.py, src/proofing_decision/crypto.py; the original test is `tests/test_proofing_decision.py::test_task_1420_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_proofing_decision_pqc.py::test_task_1420_revocation_ledger_persistence_and_cli_workflow`.
