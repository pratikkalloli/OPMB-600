# Verification

- Original: `tests/test_direct_debit.py::test_task_0801_identity_separates_signing_and_transport_keys`
- PQC reference: `tests/test_direct_debit_pqc.py::test_task_0801_identity_separates_signing_and_transport_keys`
- Procedure: create identity, ML-DSA / RSA key generation, and ML-KEM / RSA transport key generation.
- Evidence: `reports/evidence/REPO-081/test-results.json` (status remains pending until actual execution).
