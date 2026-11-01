# OPMB-4005: Verify a record signature and reject changed records

The migration must preserve the Assigns equipment operation privileges by machine class and qualification expiry; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the site_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and FarmEquipmentOperatorGrant context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
