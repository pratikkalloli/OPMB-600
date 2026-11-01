# OPMB-2242: SubscriptionRenewal public key serialization and import

## Objective

Migrate SubscriptionRenewal's An authorized subscription renewal consent receipts operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for public key serialization and import: Round-trip each public key with an explicit purpose and version tag while preserving the workflow's key contract. Preserve its domain rule that applies a workflow-specific minimum transaction quantity; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
