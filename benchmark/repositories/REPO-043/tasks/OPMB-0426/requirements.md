# OPMB-0426: PhotoVault: Seal a protected domain attachment

Replace RSA-OAEP data-key wrapping with ML-KEM-derived wrapping keys and AES-GCM, bound to the entity identifier. PhotoVault workflow: Photo object lifecycle with owner, content digest, classification, retention, and explicit sharing state. Domain-specific invariants: Photo retention must be positive and classification must use the vault policy vocabulary. The task concerns fields photo_id, owner_id, content_digest, classification, retention_days, lifecycle and legal transitions private -> shared -> revoked -> expired.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
