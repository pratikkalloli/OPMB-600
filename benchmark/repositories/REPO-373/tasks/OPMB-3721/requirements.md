# OPMB-3721: Validate the domain record and its lifecycle state

The migration must preserve the Reserves a network maintenance window and records precheck, execution, and rollback outcome; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the network_element_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and NetworkChangeWindow context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
