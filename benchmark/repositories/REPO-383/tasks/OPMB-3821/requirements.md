# OPMB-3821: Validate the domain record and its lifecycle state

The migration must preserve the Seals interval telemetry summaries with collector identity and sequence continuity; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the network_element_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and NetworkTelemetryCheckpoint context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
