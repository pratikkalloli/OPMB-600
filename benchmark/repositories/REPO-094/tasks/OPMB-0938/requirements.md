# OPMB-0938: ReferralPacket recipient-bound hybrid confidentiality

## Objective

Migrate ReferralPacket's An authorized specialist referral packet delivery operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for recipient-bound hybrid confidentiality: Establish a fresh content key with the configured key establishment mechanism, derive an AES-256-GCM key, and authenticate both ciphertext and workflow context. Preserve its domain rule that validates a clinical-purpose namespace; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
