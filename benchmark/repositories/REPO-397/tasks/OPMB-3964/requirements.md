# OPMB-3964: Sign a scoped domain record with versioned context

The migration must preserve the Preserves water sample custody, collection point, laboratory result, and quality disposition; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the site_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and WaterSampleCustody context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
