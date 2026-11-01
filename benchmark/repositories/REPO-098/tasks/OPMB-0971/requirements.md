# OPMB-0971: BiobankCustody key generation and purpose separation

## Objective

Migrate BiobankCustody's An authorized biobank sample custody transfer operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for key generation and purpose separation: Provision separate signing and transport identities for this workflow; reject key-purpose confusion. Preserve its domain rule that requires purpose-scoped clinical records; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
