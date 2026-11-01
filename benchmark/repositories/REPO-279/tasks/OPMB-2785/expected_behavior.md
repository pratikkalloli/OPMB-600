# Expected behavior

Migrate TelemetryFrameSeal verify a record signature and reject changed records from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Signs ordered telemetry frames with device and sampling-window identity to expose replay or alteration; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid telemetry frame seal operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
