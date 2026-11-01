# OPMB-3535: Verify a record signature and reject changed records

The migration must preserve the Tracks baggage custody scans between check-in, transfer, and reclaim points; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and AirportBaggageCustody context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
