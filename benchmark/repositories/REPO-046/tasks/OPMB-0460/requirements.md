# OPMB-0460: SBOMSign: Validate a domain lifecycle transition

Preserve legal domain transitions and entity-ID continuity when decision records use ML-DSA-65. SBOMSign workflow: Software bill-of-material release records with artifact digest, supplier identity, serial format, and signing state. Domain-specific invariants: SBOM release requires a lowercase SHA-256 artifact digest and supported serial format. The task concerns fields bom_id, artifact_digest, supplier_id, serial_format, created_at, verification_state and legal transitions draft -> signed -> revoked.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
