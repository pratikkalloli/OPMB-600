# OPMB-0290 requirements

Within PackageMirror's software package mirror integrity and signed indexes workflow, migrate key revocation from the RSA baseline to Fail-closed key revocation and stale-version rejection, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
