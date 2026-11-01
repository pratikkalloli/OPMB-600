# OPMB-2977: Load and validate a serialized verification key

The migration must preserve the Assigns retention and deletion schedules to device data classes with an auditable policy revision; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and IoTDataRetentionPolicy context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
