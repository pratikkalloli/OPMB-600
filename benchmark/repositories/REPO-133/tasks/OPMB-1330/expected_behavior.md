# Expected behavior

- Preserve the NameChangeProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/name_change_proof/workflow.py, src/name_change_proof/crypto.py; the original test is `tests/test_name_change_proof.py::test_task_1330_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_name_change_proof_pqc.py::test_task_1330_revocation_ledger_persistence_and_cli_workflow`.
