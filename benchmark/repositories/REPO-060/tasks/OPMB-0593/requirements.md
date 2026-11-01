# Migration requirements

- Use ML-DSA-65 with a ZoneSeal-specific context.
- Replace DER EC keys with standardized ML-DSA public-key encodings across API consumers.
- Preserve serial anti-rollback and fail-closed zone status checks.
