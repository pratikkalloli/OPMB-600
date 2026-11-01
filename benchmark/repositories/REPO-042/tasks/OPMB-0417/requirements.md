# OPMB-0417: DigitalWarranty: Open a protected domain attachment

Migrate envelope opening to ML-KEM decapsulation and preserve rejection of wrong recipients, identifiers, and tampering. DigitalWarranty workflow: Warranty claims linking product serial, claimant, evidence digest, review decision, and payment state. Domain-specific invariants: Warranty evidence must be identified by a lowercase SHA-256 digest. The task concerns fields claim_id, product_serial, claimant_id, evidence_digest, submitted_at, status and legal transitions submitted -> reviewing -> approved -> rejected -> paid.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
