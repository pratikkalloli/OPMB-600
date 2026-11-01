# OPMB-0374: ResearchRelease: Verify a domain decision

Update decision verification for ML-DSA-65 and continue rejecting modified records and invalid signatures. ResearchRelease workflow: Research dataset release approvals covering dataset digest, curator, license, and embargo lifecycle. Domain-specific invariants: Release digest must be lowercase SHA-256 and embargo time cannot be negative. The task concerns fields release_id, dataset_digest, curator_id, license_id, embargo_until, status and legal transitions draft -> approved -> published -> withdrawn.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
