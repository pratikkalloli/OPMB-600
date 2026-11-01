# OPMB-4025: Verify a record signature and reject changed records

The migration must preserve the Tracks harvest bin custody from field collection through packing intake; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the site_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and HarvestBinHandoff context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
