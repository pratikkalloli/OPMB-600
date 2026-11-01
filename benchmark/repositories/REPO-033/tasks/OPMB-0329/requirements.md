# OPMB-0329: TenantPortal: Rotate an attachment recipient

Rewrap attachment data keys for a replacement ML-KEM recipient without changing the protected payload or entity context. TenantPortal workflow: Tenant invitations and role grants with expiry, revocation, and tenant-bound encrypted evidence. Domain-specific invariants: Invitation role must be one of viewer, editor, or admin, with a positive expiration. The task concerns fields invitation_id, tenant_id, invitee_email, role, expires_at, status and legal transitions pending -> accepted -> revoked.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
