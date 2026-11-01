# OPMB-2970: Apply only an allowed domain lifecycle transition

The migration must preserve the Captures robot mission intent, completion status, and signed exception evidence; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and RobotMissionReceipt context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
