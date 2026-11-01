# Migration requirements

- Use ML-DSA-65 under a CapabilityGate-specific context.
- Migrate public-key storage and verifier interfaces; do not silently fall back to RSA.
- Preserve online revocation and expiry behavior.
