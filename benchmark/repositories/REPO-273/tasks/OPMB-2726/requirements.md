# OPMB-2726: Serialize the verification key in the algorithm format

The migration must preserve the Stages signed firmware releases by device cohort and records promotion or halt decisions; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and FirmwareRolloutRing context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
