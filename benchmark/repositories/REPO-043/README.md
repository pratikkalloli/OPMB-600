# PhotoVault

Photo object lifecycle with owner, content digest, classification, retention, and explicit sharing state. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `lifecycle` (private, shared, revoked, expired). Required fields: `photo_id`, `owner_id`, `content_digest`, `classification`, `retention_days`, `lifecycle`.

Run `python -m pytest` from this directory with the pinned requirements installed.
