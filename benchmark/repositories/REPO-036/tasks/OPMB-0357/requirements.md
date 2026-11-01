# OPMB-0357: LicenseLedger: Open a protected domain attachment

Migrate envelope opening to ML-KEM decapsulation and preserve rejection of wrong recipients, identifiers, and tampering. LicenseLedger workflow: Product license records covering organization, seats, validity windows, suspension, and revocation. Domain-specific invariants: A license must grant a positive integer seat count and positive expiry. The task concerns fields license_id, product_id, organization_id, seat_count, expires_at, status and legal transitions trial -> active -> suspended -> revoked.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
