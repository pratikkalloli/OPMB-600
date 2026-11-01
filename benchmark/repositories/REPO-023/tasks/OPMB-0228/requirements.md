# OPMB-0228 requirements

Within ConfigSign's signed configuration distribution and rollback protection workflow, migrate confidential delivery from the RSA baseline to ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
