# Verification

- Original: `tests/test_pharmacy_batch_release.py::test_task_1001_identity_separates_signing_and_transport_keys`
- PQC reference: `tests/test_pharmacy_batch_release_pqc.py::test_task_1001_identity_separates_signing_and_transport_keys`
- Procedure: create identity, ML-DSA / RSA key generation, and ML-KEM / RSA transport key generation.
- Evidence: `reports/evidence/REPO-101/test-results.json` (status remains pending until actual execution).
