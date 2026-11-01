# OPMB-0222 requirements

Within ConfigSign's signed configuration distribution and rollback protection workflow, migrate public-key serialization from the RSA baseline to Versioned DER SubjectPublicKeyInfo encoding with purpose separation, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
