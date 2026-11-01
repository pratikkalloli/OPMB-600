# OPMB-0291 requirements

Within ApprovalFlow's multi-stage approval signatures and quorum verification workflow, migrate key provisioning from the RSA baseline to ML-DSA-65 signing and ML-KEM-768 transport key generation, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
