# SBOMSign

Software bill-of-material release records with artifact digest, supplier identity, serial format, and signing state. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `verification_state` (draft, signed, revoked). Required fields: `bom_id`, `artifact_digest`, `supplier_id`, `serial_format`, `created_at`, `verification_state`.

Run `python -m pytest` from this directory with the pinned requirements installed.
