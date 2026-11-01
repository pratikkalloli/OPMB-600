# OPMB-2646: Serialize the verification key in the algorithm format

The migration must preserve the Records containment scope and the authorized release decision for material on quality hold; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the workcell_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and QualityHoldRelease context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
