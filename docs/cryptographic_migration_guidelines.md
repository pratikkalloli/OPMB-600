# Cryptographic migration guidelines

Use standardized primitives through vetted maintained libraries. RSA encryption redesign uses ML-KEM only for key establishment, a KDF for key derivation, and authenticated symmetric encryption for payloads. Preserve authentication and serialization contracts explicitly. Never implement primitives from scratch or silently substitute unsupported algorithms.
