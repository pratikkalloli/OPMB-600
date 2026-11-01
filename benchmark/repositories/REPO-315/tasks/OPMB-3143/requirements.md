# OPMB-3143: Generate an application-specific signature key pair

The migration must preserve the Records a charging session's meter start/end, station identity, and settlement state; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the asset_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and EVChargeSession context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
