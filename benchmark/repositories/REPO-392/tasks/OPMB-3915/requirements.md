# OPMB-3915: Verify a record signature and reject changed records

The migration must preserve the Tracks soil probe calibration factors and service interval for a named field location; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the site_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and SoilProbeCalibration context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
