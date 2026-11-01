# Migration requirements

- Use ML-DSA-65 with a SensorAttest-specific context.
- Replace DER EC key serialization with ML-DSA public-key encodings throughout callers.
- Preserve fail-closed signature validation, device deactivation, and replay checks.
