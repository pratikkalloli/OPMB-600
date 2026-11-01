# OPMB-1282: AuthenticatorBinding public key serialization and import

## Objective

Migrate AuthenticatorBinding's An authorized authenticator device binding records operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for public key serialization and import: Round-trip each public key with an explicit purpose and version tag while preserving the workflow's key contract. Preserve its domain rule that rejects assurance levels outside the relying-party range; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
