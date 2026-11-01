# OPMB-0277 requirements

Within DesktopUpdateProof's desktop software update integrity and signed releases workflow, migrate record verification from the RSA baseline to ML-DSA verification with tamper and context rejection, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
