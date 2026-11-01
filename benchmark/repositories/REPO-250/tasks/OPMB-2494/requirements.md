# OPMB-2494: Sign a scoped domain record with versioned context

The migration must preserve the Receiving inspection, source-lot binding, production consumption, and traceability export. business invariant and the component_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and ComponentTraceLot context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
