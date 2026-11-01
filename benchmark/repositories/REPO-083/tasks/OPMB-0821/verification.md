# Verification

- Original: `tests/test_chargeback_file.py::test_task_0821_identity_separates_signing_and_transport_keys`
- PQC reference: `tests/test_chargeback_file_pqc.py::test_task_0821_identity_separates_signing_and_transport_keys`
- Procedure: create identity, ML-DSA / RSA key generation, and ML-KEM / RSA transport key generation.
- Evidence: `reports/evidence/REPO-083/test-results.json` (status remains pending until actual execution).
