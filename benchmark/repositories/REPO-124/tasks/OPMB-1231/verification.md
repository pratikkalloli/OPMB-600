# Verification

- Original: `tests/test_cert_renewal_plan.py::test_task_1231_identity_separates_signing_and_transport_keys`
- PQC reference: `tests/test_cert_renewal_plan_pqc.py::test_task_1231_identity_separates_signing_and_transport_keys`
- Procedure: create identity, ML-DSA / RSA key generation, and ML-KEM / RSA transport key generation.
- Evidence: `reports/evidence/REPO-124/test-results.json` (status remains pending until actual execution).
