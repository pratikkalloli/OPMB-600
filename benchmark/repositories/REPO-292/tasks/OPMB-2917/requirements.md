# OPMB-2917: Load and validate a serialized verification key

The migration must preserve the Records compiler, source revision, and reproducible build digest for a microcontroller image; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and MicrocontrollerBuildProof context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
