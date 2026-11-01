# OPMB-2349: SalesTaxEvidence key rotation and retired-key policy

## Objective

Migrate SalesTaxEvidence's An authorized merchant sales tax evidence exports operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for key rotation and retired-key policy: Rotate signing and transport identities together, advance their version, and reject access through the retired version. Preserve its domain rule that enforces positive merchant quantities and a two-letter region; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
