# OPMB-0614: BeneficiaryProof domain validation and authorization policy

## Objective

Migrate BeneficiaryProof's An authorized beneficiary account changes operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state. workflow for domain validation and authorization policy: Apply the application's required fields, validity window, and domain invariant before allowing the business record to be signed. Preserve its domain rule that rejects low-value or malformed currency records; do not silently downgrade algorithms or relax validation.

## Requirements

- Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.
- Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.
- Retain the application's field validation, persistence behavior, and lifecycle policy.
