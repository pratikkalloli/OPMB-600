# OPMB-2430: Apply only an allowed domain lifecycle transition

The migration must preserve the Fixture identification, technician measurement, tolerance review, calibration certificate signing, and expiration. business invariant and the fixture_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and FixtureCalibrationDossier context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
