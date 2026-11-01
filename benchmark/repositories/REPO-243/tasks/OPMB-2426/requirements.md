# OPMB-2426: Serialize the verification key in the algorithm format

The migration must preserve the Fixture identification, technician measurement, tolerance review, calibration certificate signing, and expiration. business invariant and the fixture_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and FixtureCalibrationDossier context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
