# OPMB-2829: Recover an artifact and reject malformed or altered envelopes

The migration must preserve the Registers diagnostic probes, their allowed command set, and the evidence collected from a device; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and RemoteProbeRegistry context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
