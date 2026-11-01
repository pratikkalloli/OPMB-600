# Migration requirements

- Use standardized ML-DSA-65 with a FirmwareFleet release context.
- Update public-key serialization and all verification callers; do not fall back to RSA.
- Preserve monotonic device rollout checks and fail closed.
