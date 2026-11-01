# SecureForms

Form submissions binding schema version, submitter reference, consent version, and processing lifecycle. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `processing_state` (received, validated, sealed, rejected). Required fields: `form_id`, `submission_id`, `submitter_ref`, `schema_version`, `received_at`, `consent_version`, `processing_state`.

Run `python -m pytest` from this directory with the pinned requirements installed.
