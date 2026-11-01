# OPMB-2459: Recover an artifact and reject malformed or altered envelopes

The migration must preserve the Tool wear report, technician assignment, supervisor authorization, change confirmation, and return-to-service. business invariant and the cell_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and ToolChangeAuthorization context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
