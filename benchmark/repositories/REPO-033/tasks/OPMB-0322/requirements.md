# OPMB-0322: TenantPortal: Generate the decision signing key pair

Replace RSA decision-signing keys with ML-DSA-65 keys and keep them separate from recipient key-establishment keys. TenantPortal workflow: Tenant invitations and role grants with expiry, revocation, and tenant-bound encrypted evidence. Domain-specific invariants: Invitation role must be one of viewer, editor, or admin, with a positive expiration. The task concerns fields invitation_id, tenant_id, invitee_email, role, expires_at, status and legal transitions pending -> accepted -> revoked.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
