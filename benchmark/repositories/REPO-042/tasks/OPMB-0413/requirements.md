# OPMB-0413: DigitalWarranty: Sign a domain decision

Migrate domain decision signatures from RSA-PSS/SHA-256 to ML-DSA-65 while preserving canonical bytes and domain separation. DigitalWarranty workflow: Warranty claims linking product serial, claimant, evidence digest, review decision, and payment state. Domain-specific invariants: Warranty evidence must be identified by a lowercase SHA-256 digest. The task concerns fields claim_id, product_serial, claimant_id, evidence_digest, submitted_at, status and legal transitions submitted -> reviewing -> approved -> rejected -> paid.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
