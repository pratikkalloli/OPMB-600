# Cryptographic verification summary

Status: passed in the captured application suites; this is test evidence, not independent FIPS validation or production certification.

Environment: Python 3.11.9, pytest 8.4.2, cryptography 50.0.2.

Every PQC reference uses FIPS 204 ML-DSA-65 for signatures, FIPS 203 ML-KEM-768 for key establishment, HKDF-SHA-256 for context-specific content-key derivation, and AES-256-GCM for authenticated encryption. The classical baselines use separate RSA-3072 signing and RSA-OAEP-SHA-256 transport keys with AES-256-GCM.

Observed PQC suite results: 1800 passed; 0 failed, 0 skipped, 0 errors, 0 warnings across 180 repositories.

The tests cover key-purpose separation and serialization, malformed encoding rejection, domain validation, deterministic canonicalization, context-bound signatures, tamper and downgrade rejection, recipient and context-bound encryption, rotation, retired-key rejection, terminal revocation, persistent signed records, and CLI execution.
