# OPMB-2408: Protect a workflow artifact for an authorized recipient

The migration must preserve the Recipe authoring, quality review, controlled release, and retirement for one manufacturing workcell. business invariant and the line_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and WorkcellRecipeVault context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
