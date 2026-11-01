# OPMB-3935: Verify a record signature and reject changed records

The migration must preserve the Records seed lot origin, treatment declarations, and destination planting blocks; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the site_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and SeedLotProvenance context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
