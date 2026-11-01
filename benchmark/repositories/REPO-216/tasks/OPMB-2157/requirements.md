# OPMB-2157: MerchantOnboard signature tamper and downgrade rejection

## Objective

Migrate MerchantOnboard's An authorized marketplace merchant onboarding review operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for signature tamper and downgrade rejection: Reject altered payloads, untrusted signing keys, malformed signatures, and algorithm or version downgrade attempts. Preserve its domain rule that checks merchant region and order quantity policies; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
