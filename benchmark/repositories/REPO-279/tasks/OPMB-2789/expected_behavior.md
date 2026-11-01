# Expected behavior

Migrate TelemetryFrameSeal recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Signs ordered telemetry frames with device and sampling-window identity to expose replay or alteration; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid telemetry frame seal operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
