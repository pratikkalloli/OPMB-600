# Migration requirements

- Use standardized ML-KEM-768 for key establishment and ML-DSA-65 where metadata is signed.
- Update serialized public-key formats and callers; do not silently fall back to classical public-key cryptography.
- Retain AES-256-GCM and bind snapshot context through authenticated metadata.
