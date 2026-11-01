# OPMB-2452: Canonicalize the complete domain record for signing

The migration must preserve the Tool wear report, technician assignment, supervisor authorization, change confirmation, and return-to-service. business invariant and the cell_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and ToolChangeAuthorization context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
