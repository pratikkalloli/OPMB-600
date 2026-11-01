# OPMB-2649: Recover an artifact and reject malformed or altered envelopes

The migration must preserve the Records containment scope and the authorized release decision for material on quality hold; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the workcell_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and QualityHoldRelease context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
