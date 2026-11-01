# OPMB-0424: PhotoVault: Verify a domain decision

Update decision verification for ML-DSA-65 and continue rejecting modified records and invalid signatures. PhotoVault workflow: Photo object lifecycle with owner, content digest, classification, retention, and explicit sharing state. Domain-specific invariants: Photo retention must be positive and classification must use the vault policy vocabulary. The task concerns fields photo_id, owner_id, content_digest, classification, retention_days, lifecycle and legal transitions private -> shared -> revoked -> expired.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
