# ResearchRelease

Research dataset release approvals covering dataset digest, curator, license, and embargo lifecycle. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `status` (draft, approved, published, withdrawn). Required fields: `release_id`, `dataset_digest`, `curator_id`, `license_id`, `embargo_until`, `status`.

Run `python -m pytest` from this directory with the pinned requirements installed.
