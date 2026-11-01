# OPMB-2435: Verify a record signature and reject changed records

The migration must preserve the Procedure drafting, welding-engineer qualification, controlled issue, and supersession of a weld specification. business invariant and the joint_class scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and WeldProcedureRelease context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
