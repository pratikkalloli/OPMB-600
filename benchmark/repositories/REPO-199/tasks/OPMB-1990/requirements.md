# OPMB-1990: RegulatoryFiling revocation, persistence, and runnable workflow

## Objective

Migrate RegulatoryFiling's An authorized regulatory filing amendment tracking operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for revocation, persistence, and runnable workflow: Enforce terminal revocation, persist uniquely identified signed records, and preserve validation and signature behavior through the application's command-line flow. Preserve its domain rule that requires an increasing filing sequence and recognized custody state; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
