# OPMB-2617: Load and validate a serialized verification key

The migration must preserve the Tracks lot expiry and opened-container life for process consumables used by a production cell; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the workcell_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and ConsumableShelfLifeCard context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
