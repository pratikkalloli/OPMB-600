# OPMB-0419: DigitalWarranty: Rotate an attachment recipient

Rewrap attachment data keys for a replacement ML-KEM recipient without changing the protected payload or entity context. DigitalWarranty workflow: Warranty claims linking product serial, claimant, evidence digest, review decision, and payment state. Domain-specific invariants: Warranty evidence must be identified by a lowercase SHA-256 digest. The task concerns fields claim_id, product_serial, claimant_id, evidence_digest, submitted_at, status and legal transitions submitted -> reviewing -> approved -> rejected -> paid.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
