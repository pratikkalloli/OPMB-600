# OPMB-2760: Apply only an allowed domain lifecycle transition

The migration must preserve the Transfers a device between fictional owners while revoking the prior owner's access grant; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the device_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and DeviceOwnershipTransfer context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
