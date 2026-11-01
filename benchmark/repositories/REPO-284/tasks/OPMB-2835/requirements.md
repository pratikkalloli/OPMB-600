# OPMB-2835: Verify a record signature and reject changed records

The migration must preserve the Coordinates recovery of a lost device identity and records invalidation of its previous credentials; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and DeviceRecoveryTicket context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
