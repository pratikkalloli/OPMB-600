# OPMB-0446: APIKeyBroker: Seal a protected domain attachment

Replace RSA-OAEP data-key wrapping with ML-KEM-derived wrapping keys and AES-GCM, bound to the entity identifier. APIKeyBroker workflow: API credential lifecycle with client binding, scopes, expiry, activation, and revocation. Domain-specific invariants: API credentials require unique nonempty scopes and expiry after creation. The task concerns fields credential_id, client_id, scopes, created_at, expires_at, status and legal transitions pending -> active -> revoked -> expired.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
