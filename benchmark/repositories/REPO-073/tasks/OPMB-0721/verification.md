# Verification

- Original: `tests/test_broker_order.py::test_task_0721_identity_separates_signing_and_transport_keys`
- PQC reference: `tests/test_broker_order_pqc.py::test_task_0721_identity_separates_signing_and_transport_keys`
- Procedure: create identity, ML-DSA / RSA key generation, and ML-KEM / RSA transport key generation.
- Evidence: `reports/evidence/REPO-073/test-results.json` (status remains pending until actual execution).
