# OPMB-2750: Apply only an allowed domain lifecycle transition

The migration must preserve the Approves a sensor gateway's join request only when its hardware identity and site assignment match; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and GatewayJoinApproval context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
