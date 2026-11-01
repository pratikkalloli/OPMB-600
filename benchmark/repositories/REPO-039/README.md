# SecureQueue

Queue message delivery receipts with producer identity, lease expiry, acknowledgement, and dead-letter state. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `delivery_state` (pending, leased, acked, dead_letter). Required fields: `message_id`, `queue_name`, `producer_id`, `created_at`, `expires_at`, `delivery_state`.

Run `python -m pytest` from this directory with the pinned requirements installed.
