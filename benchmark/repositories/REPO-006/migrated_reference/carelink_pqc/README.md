# CareLink PQC reference

This synthetic reference uses `cryptography==50.0.2` standardized FIPS 204 ML-DSA-65 for operations 01–04 and 08–10, and FIPS 203 ML-KEM-768 for operations 05–07. KEM derives a 256-bit AEAD key using HKDF-SHA-256; AES-256-GCM protects payloads and authenticates protocol context. The API retains the original operation call shape. For encryption, its first key argument is the KEM public key; for decryption, its second key argument is the KEM private key.

Public keys use DER SubjectPublicKeyInfo and are type checked by purpose. Envelopes carry a version and algorithm identifier; unsupported versions, algorithm substitutions, malformed input, context mismatch, and authentication failures are rejected. ML-DSA signing keys and ML-KEM transport keys are separate. RSA interoperability is intentionally not provided. This is a synthetic benchmark implementation, not a production healthcare messaging system.
