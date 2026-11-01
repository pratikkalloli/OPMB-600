# RedactionProof

Redaction review cases linking document digests, redaction maps, reviewers, and disclosure approvals. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `status` (draft, approved, disclosed, rejected). Required fields: `case_id`, `document_digest`, `redaction_map_digest`, `reviewer_id`, `disclosure_policy`, `status`.

Run `python -m pytest` from this directory with the pinned requirements installed.
