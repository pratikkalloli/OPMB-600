# Cryptographic verification: Batches 01?18

The 180 original test suites exercise ECDSA P-256 signatures; separate reference suites exercise provider ML-DSA-65 (FIPS 204) using the pinned cryptography 50.0.2 library. Tests cover valid claims, wrong signing keys, altered persisted payloads, record identifier binding, public key serialization, malformed PQC public keys, domain validation, scoped verification and deactivation. Per-application test results and lexical post-migration scans are stored under `reports/evidence/REPO-XXX/`.

These tests and scans provide evidence of exercised behavior only. They are not formal security proofs, certification or a claim of production readiness. No confidentiality or KEM migration is claimed for these signature and integrity workflows.
