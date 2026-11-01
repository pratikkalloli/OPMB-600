# OPMB-0447: APIKeyBroker: Open a protected domain attachment

Migrate envelope opening to ML-KEM decapsulation and preserve rejection of wrong recipients, identifiers, and tampering. APIKeyBroker workflow: API credential lifecycle with client binding, scopes, expiry, activation, and revocation. Domain-specific invariants: API credentials require unique nonempty scopes and expiry after creation. The task concerns fields credential_id, client_id, scopes, created_at, expires_at, status and legal transitions pending -> active -> revoked -> expired.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
