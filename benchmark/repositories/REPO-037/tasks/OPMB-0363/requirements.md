# OPMB-0363: EdgeCacheTrust: Sign a domain decision

Migrate domain decision signatures from RSA-PSS/SHA-256 to ML-DSA-65 while preserving canonical bytes and domain separation. EdgeCacheTrust workflow: Edge cache leases binding object digests to origin validators, freshness deadlines, and trust states. Domain-specific invariants: Cache trust tier must use the explicit policy vocabulary and a positive freshness deadline. The task concerns fields lease_id, object_key, origin_digest, etag, fresh_until, trust_tier, state and legal transitions fresh -> stale -> evicted.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
