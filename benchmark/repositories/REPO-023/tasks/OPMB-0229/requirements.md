# OPMB-0229 requirements

Within ConfigSign's signed configuration distribution and rollback protection workflow, migrate key rotation from the RSA baseline to Versioned signing and transport key rotation, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
