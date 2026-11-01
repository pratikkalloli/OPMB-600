# OPMB-2882: Canonicalize the complete domain record for signing

The migration must preserve the Records production lot, calibration status, and destination for a batch of deployed sensors; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and SensorBatchProvenance context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
