# Migration requirements

- Use the standardized PQC construction named by the task and the pinned cryptography library.
- Migrate key and message serialization without silent classical fallback.
- Retain application-specific authorization, version, expiry, or sequence checks.
