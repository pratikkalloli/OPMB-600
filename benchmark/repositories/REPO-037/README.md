# EdgeCacheTrust

Edge cache leases binding object digests to origin validators, freshness deadlines, and trust states. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `state` (fresh, stale, evicted). Required fields: `lease_id`, `object_key`, `origin_digest`, `etag`, `fresh_until`, `trust_tier`, `state`.

Run `python -m pytest` from this directory with the pinned requirements installed.
