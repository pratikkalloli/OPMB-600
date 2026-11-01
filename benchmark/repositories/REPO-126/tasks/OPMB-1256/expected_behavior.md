# Expected behavior

- Preserve the FederatedClaimMap workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/federated_claim_map/workflow.py, src/federated_claim_map/crypto.py; the original test is `tests/test_federated_claim_map.py::test_task_1256_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_federated_claim_map_pqc.py::test_task_1256_signature_binds_record_context_and_validity`.
