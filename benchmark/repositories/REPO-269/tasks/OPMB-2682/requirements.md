# OPMB-2682: Canonicalize the complete domain record for signing

The migration must preserve the Tracks operator qualification scope and expiration for safety-sensitive production tasks; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the workcell_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and OperatorQualificationGrant context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
