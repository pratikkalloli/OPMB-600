# Expected behavior

- Preserve the OrgIdentityProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/org_identity_proof/workflow.py, src/org_identity_proof/crypto.py; the original test is `tests/test_org_identity_proof.py::test_task_1370_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_org_identity_proof_pqc.py::test_task_1370_revocation_ledger_persistence_and_cli_workflow`.
