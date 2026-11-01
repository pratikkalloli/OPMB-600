# OPMB-2507: Load and validate a serialized verification key

The migration must preserve the Tracks an industrial machine's identity, custodian, and maintenance attestations across controlled ownership changes; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the workcell_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and SerializedMachinePassport context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
