# LicenseLedger

Product license records covering organization, seats, validity windows, suspension, and revocation. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `status` (trial, active, suspended, revoked). Required fields: `license_id`, `product_id`, `organization_id`, `seat_count`, `expires_at`, `status`.

Run `python -m pytest` from this directory with the pinned requirements installed.
