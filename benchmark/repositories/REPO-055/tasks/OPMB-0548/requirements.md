# Migration requirements

- Use ML-DSA-65 with a mailbox-specific context for sender signatures.
- Use ML-KEM-768, HKDF-SHA-256, and AES-256-GCM for recipient encryption.
- Update serialized key formats and integration callers without classical fallback.
