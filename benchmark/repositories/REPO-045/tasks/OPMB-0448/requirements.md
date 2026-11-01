# OPMB-0448: APIKeyBroker: Encode recipient public-key material

Replace RSA PEM serialization with the pinned provider raw ML-KEM-768 public-key encoding and update consumers. APIKeyBroker workflow: API credential lifecycle with client binding, scopes, expiry, activation, and revocation. Domain-specific invariants: API credentials require unique nonempty scopes and expiry after creation. The task concerns fields credential_id, client_id, scopes, created_at, expires_at, status and legal transitions pending -> active -> revoked -> expired.

## Required changes

- Migrate the identified operation to ML-KEM-768.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
