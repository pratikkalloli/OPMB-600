# OPMB-2635: Verify a record signature and reject changed records

The migration must preserve the Carries a serialized work order through required operations and captures station-level signoff; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the workcell_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and WorkOrderTraveler context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
