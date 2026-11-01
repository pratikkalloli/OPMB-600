# OPMB-0286 requirements

Within PackageMirror's software package mirror integrity and signed indexes workflow, migrate record signing from the RSA baseline to Context-bound ML-DSA-65 signature over the canonical record, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
