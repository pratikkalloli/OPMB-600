# Migration requirements

- Use ML-DSA-65 with a LicenseDesk-specific signature context.
- Replace RSA public-key serialization and update all consumers without fallback.
- Preserve offline verification and revocation snapshot formats and semantics.
