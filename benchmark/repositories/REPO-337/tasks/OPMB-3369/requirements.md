# OPMB-3369: Recover an artifact and reject malformed or altered envelopes

The migration must preserve the Schedules bus charging against departure readiness, charger availability, and energy limits; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and BusDepotChargeDispatch context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
