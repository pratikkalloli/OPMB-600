# Expected behavior

Migrate NetworkTelemetryCheckpoint protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Seals interval telemetry summaries with collector identity and sequence continuity; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid network telemetry checkpoint operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
