# Expected behavior

- Only a valid unexpired non-revoked capability with exact principal, resource, and action scope authorizes.
- Token identifiers are unique and signed fields are integrity bound.
- Unknown issuers and altered signatures fail closed.
