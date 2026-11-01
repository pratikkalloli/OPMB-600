# OPMB-2073: DecreeMilestone strict key input validation

## Objective

Migrate DecreeMilestone's An authorized consent decree milestone reporting operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for strict key input validation: Reject malformed, unsupported-version, unsupported-algorithm, and wrong-purpose key encodings. Preserve its domain rule that accepts only recognized docket states; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
