# OPMB-3077: Load and validate a serialized verification key

The migration must preserve the Records wind turbine maintenance work, component serials, and post-service inspection; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the asset_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and TurbineMaintenanceDossier context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
