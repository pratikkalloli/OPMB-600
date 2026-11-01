# OPMB-2775: Verify a record signature and reject changed records

The migration must preserve the Captures battery cycle measurements and maintenance decisions for a battery-backed field device; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and BatteryHealthLog context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
