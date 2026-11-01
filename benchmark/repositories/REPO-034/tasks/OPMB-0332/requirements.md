# OPMB-0332: SecureClipboard: Generate the decision signing key pair

Replace RSA decision-signing keys with ML-DSA-65 keys and keep them separate from recipient key-establishment keys. SecureClipboard workflow: Short-lived clipboard shares bound to owner, recipient, sensitivity label, and expiration. Domain-specific invariants: Clipboard sensitivity must use the policy vocabulary and expiry must follow creation. The task concerns fields clip_id, owner_id, recipient_id, sensitivity, created_at, expires_at, status and legal transitions active -> revoked -> expired.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
