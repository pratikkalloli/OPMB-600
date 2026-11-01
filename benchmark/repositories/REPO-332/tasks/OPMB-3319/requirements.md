# OPMB-3319: Recover an artifact and reject malformed or altered envelopes

The migration must preserve the Records refrigerated shipment custody transfer with temperature range and seal condition; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and ColdChainTransfer context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
