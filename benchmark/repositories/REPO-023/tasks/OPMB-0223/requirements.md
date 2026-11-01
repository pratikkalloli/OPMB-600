# OPMB-0223 requirements

Within ConfigSign's signed configuration distribution and rollback protection workflow, migrate public-key loading from the RSA baseline to Strict ML-DSA/ML-KEM public-key decoding and type validation, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
