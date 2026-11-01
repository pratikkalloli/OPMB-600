# SecureClipboard

Short-lived clipboard shares bound to owner, recipient, sensitivity label, and expiration. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `status` (active, revoked, expired). Required fields: `clip_id`, `owner_id`, `recipient_id`, `sensitivity`, `created_at`, `expires_at`, `status`.

Run `python -m pytest` from this directory with the pinned requirements installed.
