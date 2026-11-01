# OPMB-0204 requirements

Within MailGuard's secure email envelopes and attachments workflow, migrate business validation from the RSA baseline to Domain-specific input and authorization preconditions, preserving the application contract and rejecting invalid or downgraded inputs.

- Preserve domain validation and the existing call shape.
- Use the standardized target named in task metadata.
- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.
- Keep signing and key-establishment keys separate.
