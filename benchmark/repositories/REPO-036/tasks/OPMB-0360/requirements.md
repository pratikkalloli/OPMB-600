# OPMB-0360: LicenseLedger: Validate a domain lifecycle transition

Preserve legal domain transitions and entity-ID continuity when decision records use ML-DSA-65. LicenseLedger workflow: Product license records covering organization, seats, validity windows, suspension, and revocation. Domain-specific invariants: A license must grant a positive integer seat count and positive expiry. The task concerns fields license_id, product_id, organization_id, seat_count, expires_at, status and legal transitions trial -> active -> suspended -> revoked.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
