# OPMB-2415: Verify a record signature and reject changed records

The migration must preserve the Changeover checklist, supervisor approval, release token issuance, and later revocation for a production line. business invariant and the line_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and LineClearanceToken context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
