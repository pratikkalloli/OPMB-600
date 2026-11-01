# OPMB-2475: Verify a record signature and reject changed records

The migration must preserve the Deviation intake, severity assignment, containment, disposition approval, and closure evidence. business invariant and the production_order scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and ProductionDeviationCase context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
