# OPMB-3338: Protect a workflow artifact for an authorized recipient

The migration must preserve the Binds container identity, seal changes, and authorized port custody events; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and PortContainerSeal context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
