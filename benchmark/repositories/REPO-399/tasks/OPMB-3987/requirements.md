# OPMB-3987: Load and validate a serialized verification key

The migration must preserve the Records environmental station calibration checks and correction factors; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the site_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and WeatherStationCalibration context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
