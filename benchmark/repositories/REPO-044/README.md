# KeyRecovery

Threshold recovery cases tracking principal, key fingerprint, required approvals, and fulfillment decisions. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `recovery_state` (opened, approved, fulfilled, denied). Required fields: `recovery_id`, `principal_id`, `key_fingerprint`, `approvals_required`, `opened_at`, `recovery_state`.

Run `python -m pytest` from this directory with the pinned requirements installed.
