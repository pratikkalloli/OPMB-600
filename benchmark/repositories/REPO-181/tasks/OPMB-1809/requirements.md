# OPMB-1809: EvidenceCustodyChain key rotation and retired-key policy

## Objective

Migrate EvidenceCustodyChain's An authorized forensic evidence custody handoffs operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for key rotation and retired-key policy: Rotate signing and transport identities together, advance their version, and reject access through the retired version. Preserve its domain rule that requires an increasing filing sequence and recognized custody state; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
