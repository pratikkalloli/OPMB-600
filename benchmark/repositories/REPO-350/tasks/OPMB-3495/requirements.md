# OPMB-3495: Verify a record signature and reject changed records

The migration must preserve the Dispatches a service vehicle to a verified breakdown location with changing assignment history; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and RoadsideAssistanceDispatch context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
