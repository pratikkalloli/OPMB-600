# Verification

- Original: `tests/test_credential_status_list.py::test_task_1311_identity_separates_signing_and_transport_keys`
- PQC reference: `tests/test_credential_status_list_pqc.py::test_task_1311_identity_separates_signing_and_transport_keys`
- Procedure: create identity, ML-DSA / RSA key generation, and ML-KEM / RSA transport key generation.
- Evidence: `reports/evidence/REPO-132/test-results.json` (status remains pending until actual execution).
