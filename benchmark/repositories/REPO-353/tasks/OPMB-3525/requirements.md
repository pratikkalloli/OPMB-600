# OPMB-3525: Verify a record signature and reject changed records

The migration must preserve the Records hazardous cargo classification, packaging checks, and carrier acceptance; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and ShippingHazardDeclaration context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
