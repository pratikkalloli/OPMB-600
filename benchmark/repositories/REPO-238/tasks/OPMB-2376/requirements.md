# OPMB-2376: VendorBankChange context-bound record signatures

## Objective

Migrate VendorBankChange's An authorized supplier bank detail change verification operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for context-bound record signatures: Sign the canonical business record with the approved signature key and bind verification to application context and record validity. Preserve its domain rule that requires region-scoped commerce evidence; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
