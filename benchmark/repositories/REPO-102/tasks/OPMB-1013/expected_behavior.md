# Expected behavior

- Preserve the VaccineColdChain workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/vaccine_cold_chain/workflow.py, src/vaccine_cold_chain/crypto.py; the original test is `tests/test_vaccine_cold_chain.py::test_task_1013_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_vaccine_cold_chain_pqc.py::test_task_1013_malformed_serialization_and_wrong_purpose_are_rejected`.
