# Migration requirements

- Use ML-DSA-65 with an application-specific context for approval signatures.
- Use ML-KEM-768, HKDF-SHA-256, and AES-256-GCM for receiving-desk transfer sealing.
- Update key serialization and integration callers without silent classical fallback.
