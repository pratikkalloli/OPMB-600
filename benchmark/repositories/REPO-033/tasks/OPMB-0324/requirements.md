# OPMB-0324: TenantPortal: Verify a domain decision

Update decision verification for ML-DSA-65 and continue rejecting modified records and invalid signatures. TenantPortal workflow: Tenant invitations and role grants with expiry, revocation, and tenant-bound encrypted evidence. Domain-specific invariants: Invitation role must be one of viewer, editor, or admin, with a positive expiration. The task concerns fields invitation_id, tenant_id, invitee_email, role, expires_at, status and legal transitions pending -> accepted -> revoked.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
