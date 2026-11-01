# OPMB-2886: Serialize the verification key in the algorithm format

The migration must preserve the Records production lot, calibration status, and destination for a batch of deployed sensors; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and SensorBatchProvenance context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
