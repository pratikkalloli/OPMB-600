# OPMB-0341: RedactionProof: Validate and canonicalize the domain entity

Preserve required fields, canonical encoding, identifier binding, and legal lifecycle states as signed domain records migrate. RedactionProof workflow: Redaction review cases linking document digests, redaction maps, reviewers, and disclosure approvals. Domain-specific invariants: Document and redaction-map commitments must be lowercase SHA-256 digests. The task concerns fields case_id, document_digest, redaction_map_digest, reviewer_id, disclosure_policy, status and legal transitions draft -> approved -> disclosed -> rejected.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
