# OPMB-3584: Sign a scoped domain record with versioned context

The migration must preserve the Versions train consist order and checks vehicle compatibility before departure; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and TrainConsistRevision context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
