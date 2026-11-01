# OPMB-0326: TenantPortal: Seal a protected domain attachment

Replace RSA-OAEP data-key wrapping with ML-KEM-derived wrapping keys and AES-GCM, bound to the entity identifier. TenantPortal workflow: Tenant invitations and role grants with expiry, revocation, and tenant-bound encrypted evidence. Domain-specific invariants: Invitation role must be one of viewer, editor, or admin, with a positive expiration. The task concerns fields invitation_id, tenant_id, invitee_email, role, expires_at, status and legal transitions pending -> accepted -> revoked.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
