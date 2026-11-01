# OPMB-0338: SecureClipboard: Encode recipient public-key material

Replace RSA PEM serialization with the pinned provider raw ML-KEM-768 public-key encoding and update consumers. SecureClipboard workflow: Short-lived clipboard shares bound to owner, recipient, sensitivity label, and expiration. Domain-specific invariants: Clipboard sensitivity must use the policy vocabulary and expiry must follow creation. The task concerns fields clip_id, owner_id, recipient_id, sensitivity, created_at, expires_at, status and legal transitions active -> revoked -> expired.

## Required changes

- Migrate the identified operation to ML-KEM-768.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
