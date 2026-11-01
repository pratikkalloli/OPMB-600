# Expected behavior

- Preserve the ContractAmendment workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/contract_amendment/workflow.py, src/contract_amendment/crypto.py; the original test is `tests/test_contract_amendment.py::test_task_2161_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_contract_amendment_pqc.py::test_task_2161_identity_separates_signing_and_transport_keys`.
