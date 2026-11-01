# OPMB-2116: SupplierInvoiceMatch context-bound record signatures

## Objective

Migrate SupplierInvoiceMatch's An authorized supplier invoice three-way matching operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for context-bound record signatures: Sign the canonical business record with the approved signature key and bind verification to application context and record validity. Preserve its domain rule that rejects zero quantity orders and malformed regions; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
