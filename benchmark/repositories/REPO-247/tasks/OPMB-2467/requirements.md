# OPMB-2467: Load and validate a serialized verification key

The migration must preserve the Room readiness, exposure-window capture, contamination review, process release, and incident quarantine. business invariant and the room_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and CleanroomProcessTicket context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
