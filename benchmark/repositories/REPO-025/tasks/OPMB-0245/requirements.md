# OPMB-0245 requirements

Within MediaRights's protected media distribution and signed rights manifests workflow, migrate canonical representation from the RSA baseline to Stable canonical JSON for signature input, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
