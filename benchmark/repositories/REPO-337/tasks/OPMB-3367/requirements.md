# OPMB-3367: Load and validate a serialized verification key

The migration must preserve the Schedules bus charging against departure readiness, charger availability, and energy limits; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and BusDepotChargeDispatch context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
