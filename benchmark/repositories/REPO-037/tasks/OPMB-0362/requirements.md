# OPMB-0362: EdgeCacheTrust: Generate the decision signing key pair

Replace RSA decision-signing keys with ML-DSA-65 keys and keep them separate from recipient key-establishment keys. EdgeCacheTrust workflow: Edge cache leases binding object digests to origin validators, freshness deadlines, and trust states. Domain-specific invariants: Cache trust tier must use the explicit policy vocabulary and a positive freshness deadline. The task concerns fields lease_id, object_key, origin_digest, etag, fresh_until, trust_tier, state and legal transitions fresh -> stale -> evicted.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
