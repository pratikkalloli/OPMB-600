# OPMB-0366: EdgeCacheTrust: Seal a protected domain attachment

Replace RSA-OAEP data-key wrapping with ML-KEM-derived wrapping keys and AES-GCM, bound to the entity identifier. EdgeCacheTrust workflow: Edge cache leases binding object digests to origin validators, freshness deadlines, and trust states. Domain-specific invariants: Cache trust tier must use the explicit policy vocabulary and a positive freshness deadline. The task concerns fields lease_id, object_key, origin_digest, etag, fresh_until, trust_tier, state and legal transitions fresh -> stale -> evicted.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
