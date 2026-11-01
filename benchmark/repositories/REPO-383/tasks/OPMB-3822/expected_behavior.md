# Expected behavior

Migrate NetworkTelemetryCheckpoint canonicalize the complete domain record for signing from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Seals interval telemetry summaries with collector identity and sequence continuity; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid network telemetry checkpoint operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
