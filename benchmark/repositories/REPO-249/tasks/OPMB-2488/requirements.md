# OPMB-2488: Protect a workflow artifact for an authorized recipient

The migration must preserve the Safety-case review, interlock epoch issuance, operator acknowledgment, and restart authorization. business invariant and the machine_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and MachineInterlockPermit context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
