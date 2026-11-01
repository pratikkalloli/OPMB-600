# OPMB-1005: PharmacyBatchRelease canonical record serialization

## Objective

Migrate PharmacyBatchRelease's An authorized pharmacy compounding batch release operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for canonical record serialization: Produce stable canonical bytes for equivalent records regardless of field insertion order. Preserve its domain rule that enforces the workflow's minimum sequence; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
